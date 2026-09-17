"""Logique métier des labs éphémères et contrôle d'ownership côté serveur."""
import hashlib
import json
import secrets
import uuid

from app.core.exceptions import ForbiddenError, NotFoundError, UnauthorizedError, ValidationError
from app.core.redis import get_redis_client
from app.integrations.github.client import create_codespace, delete_codespace, stop_codespace
from app.integrations.github.exceptions import GitHubCodespacesError
from app.modules.exercises import repository as exercises_repo
from app.modules.labs import repository as labs_repo
from app.modules.labs.schemas import LabCreateRequest, LabSessionOut, LabWebSocketTicketOut
from app.services.audit_service import log_action

CODESPACES_TTL_SECONDS = 1800
WS_TICKET_TTL_SECONDS = 60


def _ticket_key(ticket: str) -> str:
    digest = hashlib.sha256(ticket.encode("utf-8")).hexdigest()
    return f"lab_ws_ticket:{digest}"


def _owner_id(session: dict) -> uuid.UUID:
    """Convertit l'identifiant propriétaire stocké dans Redis en UUID."""
    try:
        return uuid.UUID(str(session["user_id"]))
    except (KeyError, ValueError, TypeError) as exc:
        # Une session corrompue ne doit jamais être traitée comme une session publique.
        raise NotFoundError("Session de lab introuvable ou invalide.") from exc


def get_owned_lab(lab_id: str, user_id: uuid.UUID) -> dict:
    """Récupère un lab et vérifie son propriétaire côté serveur.

    Cette fonction est le point de contrôle unique utilisé par toutes les opérations
    REST et WebSocket. Aucun identifiant fourni par le client ne peut remplacer
    `user_id`, qui provient du token d'authentification vérifié.
    """
    session = labs_repo.get_session(lab_id)
    if session is None:
        raise NotFoundError("Session de lab introuvable ou expirée.")
    if _owner_id(session) != user_id:
        raise ForbiddenError("Cette session de lab ne vous appartient pas.")
    return session


def create_ws_ticket(lab_id: str, user_id: uuid.UUID) -> LabWebSocketTicketOut:
    """Émet un ticket opaque à usage unique pour le terminal d'un Lab possédé."""
    session = get_owned_lab(lab_id, user_id)
    if session.get("status") in {"stopped", "destroyed"}:
        raise ForbiddenError("Ce lab n'accepte plus de connexion terminal.")

    ticket = secrets.token_urlsafe(32)
    payload = json.dumps({"lab_id": lab_id, "user_id": str(user_id)}, separators=(",", ":"))
    get_redis_client().set(_ticket_key(ticket), payload, ex=WS_TICKET_TTL_SECONDS)
    return LabWebSocketTicketOut(ticket=ticket, expires_in_seconds=WS_TICKET_TTL_SECONDS)


def consume_ws_ticket(ticket: str) -> tuple[str, uuid.UUID]:
    """Consomme atomiquement un ticket, puis revalide ownership et état du Lab."""
    if not ticket or len(ticket) > 256:
        raise UnauthorizedError("Ticket WebSocket invalide ou expiré.")

    redis_client = get_redis_client()
    key = _ticket_key(ticket)
    # GETDEL empêche deux connexions concurrentes de consommer le même ticket.
    raw = redis_client.getdel(key) if hasattr(redis_client, "getdel") else None
    if raw is None:
        # Fallback uniquement pour les doubles de test/anciens Redis ; la production
        # doit fournir Redis >= 6.2 pour garantir l'atomicité de GETDEL.
        raw = redis_client.get(key)
        if raw is not None:
            redis_client.delete(key)
    if not raw:
        raise UnauthorizedError("Ticket WebSocket invalide ou expiré.")

    try:
        data = json.loads(raw)
        lab_id = str(data["lab_id"])
        user_id = uuid.UUID(str(data["user_id"]))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise UnauthorizedError("Ticket WebSocket invalide ou expiré.") from exc

    session = get_owned_lab(lab_id, user_id)
    if session.get("status") in {"stopped", "destroyed"}:
        raise ForbiddenError("Ce lab n'accepte plus de connexion terminal.")
    return lab_id, user_id


def create_lab(db, payload: LabCreateRequest, user_id: uuid.UUID) -> LabSessionOut:
    exercise = exercises_repo.get_by_id(db, payload.exercise_id)
    if exercise is None:
        raise NotFoundError("Exercice introuvable.")

    if payload.kind == "judge0":
        # Judge0 n'a pas de session persistante : chaque soumission est une sandbox isolée
        # (voir exercises.service.run_code). On expose ici un identifiant logique pour le
        # frontend/terminal xterm.js uniquement.
        lab_id = f"judge0-{uuid.uuid4().hex[:12]}"
        labs_repo.save_session(lab_id, {"user_id": str(user_id), "exercise_id": str(payload.exercise_id), "kind": "judge0", "status": "ready"})
        log_action(db, user_id=user_id, action="lab.created", module="labs", resource="lab", resource_id=lab_id)
        return LabSessionOut(lab_id=lab_id, kind="judge0", status="ready", expires_in_seconds=CODESPACES_TTL_SECONDS)

    if payload.kind == "codespaces":
        if not payload.repository:
            raise ValidationError("Le paramètre 'repository' est requis pour un lab Codespaces.")
        try:
            result = create_codespace(payload.repository)
        except GitHubCodespacesError as exc:
            raise ValidationError(str(exc)) from exc

        labs_repo.save_session(result["id"], {"user_id": str(user_id), "exercise_id": str(payload.exercise_id), "kind": "codespaces", "status": result.get("state", "starting")})
        log_action(db, user_id=user_id, action="lab.created", module="labs", resource="lab", resource_id=result["id"])
        return LabSessionOut(lab_id=result["id"], kind="codespaces", status=result.get("state", "starting"), web_url=result.get("web_url"), expires_in_seconds=CODESPACES_TTL_SECONDS)

    raise ValidationError(f"Type de lab non supporté : {payload.kind}")


def _to_output(lab_id: str, session: dict) -> LabSessionOut:
    return LabSessionOut(
        lab_id=lab_id,
        kind=session["kind"],
        status=session.get("status", "active"),
        web_url=session.get("web_url"),
        expires_in_seconds=CODESPACES_TTL_SECONDS,
    )


def get_status(lab_id: str, user_id: uuid.UUID) -> LabSessionOut:
    session = get_owned_lab(lab_id, user_id)
    return _to_output(lab_id, session)


def start_lab(lab_id: str, user_id: uuid.UUID) -> LabSessionOut:
    session = get_owned_lab(lab_id, user_id)
    labs_repo.touch_session(lab_id)
    session["status"] = "active"
    labs_repo.save_session(lab_id, session)
    return _to_output(lab_id, session)


def reset_lab(lab_id: str, user_id: uuid.UUID) -> LabSessionOut:
    session = get_owned_lab(lab_id, user_id)
    labs_repo.touch_session(lab_id)
    session["status"] = "ready"
    labs_repo.save_session(lab_id, session)
    return _to_output(lab_id, session)


def stop_lab(lab_id: str, user_id: uuid.UUID) -> None:
    session = get_owned_lab(lab_id, user_id)
    if session.get("kind") == "codespaces":
        try:
            stop_codespace(lab_id)
        except GitHubCodespacesError:
            pass
    session["status"] = "stopped"
    labs_repo.save_session(lab_id, session)


def destroy_lab(db, lab_id: str, user_id: uuid.UUID) -> None:
    session = get_owned_lab(lab_id, user_id)
    if session.get("kind") == "codespaces":
        try:
            delete_codespace(lab_id)
        except GitHubCodespacesError:
            pass
    labs_repo.delete_session(lab_id)
    log_action(db, user_id=user_id, action="lab.destroyed", module="labs", resource="lab", resource_id=lab_id)
