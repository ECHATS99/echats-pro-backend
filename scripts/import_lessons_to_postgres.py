"""One-shot curriculum importer: source text files -> PostgreSQL.

Safety contract:
- ``--dry-run`` is the default and performs no database writes.
- ``--apply`` is explicit and uses one transaction with rollback on failure.
- Source bytes are never rewritten; the original UTF-8 text is embedded verbatim
  in a clearly labelled section of Lesson.content and its SHA-256 is checked.
- Quiz corrections are stored only in Answer.correct and are not returned by the
  public quiz service. The script never exposes a frontend payload.
- Existing records are reused only on an exact stable match (parent + order +
  title). Conflicting records block the apply instead of being overwritten.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

ALLOWED_DIFFICULTIES = {"beginner", "intermediate", "advanced"}
ALLOWED_QUESTION_TYPES = {"single_choice", "multi_choice", "true_false"}


class ImportInputError(RuntimeError):
    pass


@dataclass
class LessonPlan:
    item: dict[str, Any]
    source_path: Path
    enrichment_path: Path
    quiz_path: Path
    source_sha256: str
    source_text: str
    enrichment_text: str
    quiz: dict[str, Any]
    content: str
    warnings: list[str] = field(default_factory=list)


@dataclass
class CurriculumPlan:
    manifest_path: Path
    track: dict[str, Any]
    modules: list[dict[str, Any]]
    lessons: list[LessonPlan]
    warnings: list[str] = field(default_factory=list)


# Lazy imports keep --help and offline dry-runs usable without constructing an
# engine. Database dependencies are loaded only for --apply.
SessionLocal = None
Track = CourseModule = Lesson = Quiz = Question = Answer = None


def load_backend_dependencies() -> None:
    global SessionLocal, Track, CourseModule, Lesson, Quiz, Question, Answer
    from app.core.database import SessionLocal as session_factory
    from app.models.course_module import CourseModule as module_model
    from app.models.lesson import Lesson as lesson_model
    from app.models.quiz import Answer as answer_model
    from app.models.quiz import Question as question_model
    from app.models.quiz import Quiz as quiz_model
    from app.models.track import Track as track_model

    SessionLocal = session_factory
    Track = track_model
    CourseModule = module_model
    Lesson = lesson_model
    Quiz = quiz_model
    Question = question_model
    Answer = answer_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Valider les sources et afficher le plan sans écrire (mode par défaut).",
    )
    mode.add_argument(
        "--apply",
        action="store_true",
        help="Écrire le track, les modules, les leçons et les quiz dans PostgreSQL.",
    )
    parser.add_argument("--manifest", required=True, help="Chemin vers curriculum_manifest.json.")
    parser.add_argument(
        "--source-dir",
        default=None,
        help="Dossier racine contenant les fichiers sources et les sous-dossiers enrichments/quizzes-private.",
    )
    parser.add_argument("--max-details", type=int, default=200, help="Nombre maximal de détails dans la sortie JSON.")
    return parser.parse_args()


def require_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ImportInputError(f"Champ manifeste invalide ou absent: {field_name}")
    return value.strip()


def resolve_path(raw: str, manifest_dir: Path, source_dir: Path | None) -> Path:
    candidate = Path(raw)
    if candidate.is_file():
        return candidate
    if source_dir is not None:
        candidate = source_dir / raw
        if candidate.is_file():
            return candidate
    candidate = manifest_dir / raw
    if candidate.is_file():
        return candidate
    raise ImportInputError(f"Fichier introuvable: {raw}")


def source_and_digest(path: Path, expected: str) -> tuple[str, str]:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected:
        raise ImportInputError(
            f"Checksum différent pour {path.name}: manifeste={expected}, calculé={digest}. Import arrêté."
        )
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ImportInputError(f"Source non UTF-8: {path}") from exc
    return text, digest


def validate_quiz(quiz: Any, lesson_slug: str) -> dict[str, Any]:
    if not isinstance(quiz, dict):
        raise ImportInputError(f"Quiz invalide pour {lesson_slug}: objet JSON attendu.")
    if quiz.get("format") != "ECHATS_QUIZ_IMPORT_V1":
        raise ImportInputError(f"Format de quiz invalide pour {lesson_slug}.")
    if quiz.get("lesson_slug") != lesson_slug:
        raise ImportInputError(f"Quiz {lesson_slug}: lesson_slug incohérent.")
    title = require_string(quiz.get("title"), f"quiz.{lesson_slug}.title")
    passing_score = quiz.get("passing_score", 75)
    if not isinstance(passing_score, int) or not 0 <= passing_score <= 100:
        raise ImportInputError(f"Quiz {lesson_slug}: passing_score doit être entre 0 et 100.")
    questions = quiz.get("questions")
    if not isinstance(questions, list) or not 10 <= len(questions) <= 15:
        raise ImportInputError(f"Quiz {lesson_slug}: 10 à 15 questions sont requises.")
    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            raise ImportInputError(f"Quiz {lesson_slug}, question {index}: objet attendu.")
        text = require_string(question.get("question"), f"quiz.{lesson_slug}.questions[{index}].question")
        if len(text) > 1000:
            raise ImportInputError(f"Quiz {lesson_slug}, question {index}: texte trop long.")
        kind = require_string(question.get("type"), f"quiz.{lesson_slug}.questions[{index}].type")
        if kind not in ALLOWED_QUESTION_TYPES:
            raise ImportInputError(f"Quiz {lesson_slug}, question {index}: type non supporté {kind}.")
        answers = question.get("answers")
        if not isinstance(answers, list) or len(answers) < 2:
            raise ImportInputError(f"Quiz {lesson_slug}, question {index}: au moins deux réponses sont requises.")
        correct_count = 0
        for answer_index, answer in enumerate(answers, start=1):
            if not isinstance(answer, dict):
                raise ImportInputError(f"Quiz {lesson_slug}, question {index}, réponse {answer_index}: objet attendu.")
            answer_text = require_string(answer.get("answer"), "answer")
            if len(answer_text) > 500:
                raise ImportInputError(f"Quiz {lesson_slug}, question {index}, réponse {answer_index}: texte trop long.")
            if not isinstance(answer.get("correct"), bool):
                raise ImportInputError(f"Quiz {lesson_slug}, question {index}, réponse {answer_index}: correct doit être booléen.")
            correct_count += int(answer["correct"])
        if kind == "single_choice" and correct_count != 1:
            raise ImportInputError(f"Quiz {lesson_slug}, question {index}: single_choice exige une seule réponse correcte.")
        if kind == "multi_choice" and correct_count < 1:
            raise ImportInputError(f"Quiz {lesson_slug}, question {index}: multi_choice exige au moins une réponse correcte.")
        if kind == "true_false" and len(answers) != 2:
            raise ImportInputError(f"Quiz {lesson_slug}, question {index}: true_false exige deux réponses.")
    return {"title": title, "passing_score": passing_score, "questions": questions}


def build_content(item: dict[str, Any], source_text: str, enrichment_text: str, digest: str) -> str:
    title = require_string(item.get("title"), "lesson.title")
    return (
        "# Parcours enrichi — " + title + "\n\n"
        "> Cette enveloppe pédagogique est ajoutée par l’importateur. Le contenu source ci-dessous est conservé verbatim.\n\n"
        + enrichment_text.rstrip()
        + "\n\n---\n\n"
        "## Contenu source original (préservé)\n\n"
        f"> Fichier source : `{item['source_file']}`  \n> SHA-256 : `{digest}`\n\n"
        + source_text
    )


def build_plan(args: argparse.Namespace) -> CurriculumPlan:
    manifest_path = Path(args.manifest).expanduser().resolve()
    if not manifest_path.is_file():
        raise ImportInputError(f"Manifeste absent: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ImportInputError(f"Manifeste JSON invalide: {manifest_path}") from exc
    if manifest.get("format") != "ECHATS_CURRICULUM_MANIFEST_V1":
        raise ImportInputError("Format de manifeste non supporté.")
    track = manifest.get("track")
    if not isinstance(track, dict):
        raise ImportInputError("Le manifeste doit contenir un track.")
    track_slug = require_string(track.get("slug"), "track.slug")
    track_title = require_string(track.get("title"), "track.title")
    if len(track_slug) > 220 or len(track_title) > 200:
        raise ImportInputError("Track trop long.")
    modules = manifest.get("modules")
    lessons = manifest.get("lessons")
    if not isinstance(modules, list) or not modules:
        raise ImportInputError("Le manifeste ne contient aucun module.")
    if not isinstance(lessons, list) or not lessons:
        raise ImportInputError("Le manifeste ne contient aucune leçon.")
    module_keys: set[str] = set()
    for module in modules:
        key = require_string(module.get("slug"), "module.slug")
        title = require_string(module.get("title"), "module.title")
        order = module.get("order")
        if key in module_keys or not isinstance(order, int) or order < 1:
            raise ImportInputError(f"Module incohérent ou doublonné: {key}")
        if len(title) > 200:
            raise ImportInputError(f"Titre de module trop long: {key}")
        module_keys.add(key)
    source_dir = Path(args.source_dir).expanduser().resolve() if args.source_dir else None
    plans: list[LessonPlan] = []
    lesson_keys: set[tuple[str, int]] = set()
    warnings: list[str] = []
    for item in lessons:
        slug = require_string(item.get("slug"), "lesson.slug")
        module_slug = require_string(item.get("module"), f"lesson.{slug}.module")
        title = require_string(item.get("title"), f"lesson.{slug}.title")
        order = item.get("order")
        difficulty = item.get("difficulty")
        duration = item.get("duration_minutes")
        if module_slug not in module_keys:
            raise ImportInputError(f"Leçon {slug}: module absent du manifeste.")
        if not isinstance(order, int) or order < 1 or (module_slug, order) in lesson_keys:
            raise ImportInputError(f"Leçon doublonnée ou ordre invalide: {module_slug}/{order}")
        if difficulty not in ALLOWED_DIFFICULTIES or not isinstance(duration, int) or duration <= 0:
            raise ImportInputError(f"Métadonnées invalides pour la leçon {slug}.")
        source_file = require_string(item.get("source_file") or item.get("source_path"), f"lesson.{slug}.source_file")
        enrichment_file = require_string(item.get("enrichment_file") or item.get("enrichment_path"), f"lesson.{slug}.enrichment_file")
        quiz_file = require_string(item.get("quiz_file") or item.get("quiz_path"), f"lesson.{slug}.quiz_file")
        source_path = resolve_path(source_file, manifest_path.parent, source_dir)
        enrichment_path = resolve_path(enrichment_file, manifest_path.parent, source_dir)
        quiz_path = resolve_path(quiz_file, manifest_path.parent, source_dir)
        expected_digest = require_string(item.get("source_sha256"), f"lesson.{slug}.source_sha256")
        source_text, digest = source_and_digest(source_path, expected_digest)
        enrichment_text = enrichment_path.read_text(encoding="utf-8")
        quiz = validate_quiz(json.loads(quiz_path.read_text(encoding="utf-8")), slug)
        lesson_warnings: list[str] = []
        if item.get("preamble"):
            lesson_warnings.append("préambule conversationnel avant le contenu pédagogique; conservé et signalé")
        if "# " not in source_text:
            lesson_warnings.append("titre Markdown non détecté")
        if len(enrichment_text.strip()) < 200:
            lesson_warnings.append("enrichissement très court")
        warnings.extend(f"{slug}: {warning}" for warning in lesson_warnings)
        plans.append(LessonPlan(item, source_path, enrichment_path, quiz_path, digest, source_text, enrichment_text, quiz, build_content(item, source_text, enrichment_text, digest), lesson_warnings))
        lesson_keys.add((module_slug, order))
    return CurriculumPlan(manifest_path, {**track, "slug": track_slug, "title": track_title}, modules, plans, warnings)


def dry_run_payload(plan: CurriculumPlan, max_details: int) -> dict[str, Any]:
    module_payload = []
    for module in sorted(plan.modules, key=lambda x: x["order"]):
        module_lessons = [x for x in plan.lessons if x.item["module"] == module["slug"]]
        module_payload.append({
            "slug": module["slug"],
            "title": module["title"],
            "order": module["order"],
            "lesson_count": len(module_lessons),
            "lessons": [
                {
                    "slug": lesson.item["slug"],
                    "title": lesson.item["title"],
                    "order": lesson.item["order"],
                    "difficulty": lesson.item["difficulty"],
                    "duration_minutes": lesson.item["duration_minutes"],
                    "source_file": lesson.item["source_file"],
                    "source_bytes": len(lesson.source_text.encode("utf-8")),
                    "source_sha256": lesson.source_sha256,
                    "preamble_warning": bool(lesson.item.get("preamble")),
                    "quiz_questions": len(lesson.quiz["questions"]),
                    "enrichment_bytes": len(lesson.enrichment_text.encode("utf-8")),
                    "warnings": lesson.warnings,
                }
                for lesson in sorted(module_lessons, key=lambda x: x.item["order"])
            ],
        })
    return {
        "mode": "dry-run",
        "writes_performed": False,
        "status": "ready",
        "manifest": str(plan.manifest_path),
        "track": {"slug": plan.track["slug"], "title": plan.track["title"], "module_count": len(plan.modules)},
        "modules": module_payload,
        "totals": {
            "tracks": 1,
            "modules": len(plan.modules),
            "lessons": len(plan.lessons),
            "quizzes": len(plan.lessons),
            "questions": sum(len(x.quiz["questions"]) for x in plan.lessons),
            "source_bytes_utf8": sum(len(x.source_text.encode("utf-8")) for x in plan.lessons),
            "enrichment_bytes_utf8": sum(len(x.enrichment_text.encode("utf-8")) for x in plan.lessons),
        },
        "warnings": plan.warnings[:max_details],
    }


def one_or_none(db, statement, label: str):
    rows = list(db.execute(statement).scalars().all())
    if len(rows) > 1:
        raise ImportInputError(f"Conflit d’idempotence: plusieurs enregistrements pour {label}.")
    return rows[0] if rows else None


def apply_plan(plan: CurriculumPlan) -> dict[str, Any]:
    if not os.getenv("DATABASE_URL", "").strip():
        raise ImportInputError("DATABASE_URL absente; aucun apply possible.")
    load_backend_dependencies()
    db = SessionLocal()
    created = {"tracks": 0, "modules": 0, "lessons": 0, "quizzes": 0, "questions": 0, "answers": 0}
    reused = {"tracks": 0, "modules": 0, "lessons": 0, "quizzes": 0}
    try:
        with db.begin():
            from sqlalchemy import select
            track = one_or_none(db, select(Track).where(Track.slug == plan.track["slug"]), f"track {plan.track['slug']}")
            if track is None:
                track = Track(title=plan.track["title"], slug=plan.track["slug"], description=plan.track.get("description"), difficulty=plan.track.get("difficulty", "advanced"), domain=plan.track.get("domain"), duration_minutes=sum(x.item["duration_minutes"] for x in plan.lessons), published=False)
                db.add(track)
                db.flush()
                created["tracks"] += 1
            else:
                reused["tracks"] += 1
                if track.title != plan.track["title"]:
                    raise ImportInputError("Track existant avec même slug mais titre différent.")
            module_by_slug: dict[str, Any] = {}
            for module_item in sorted(plan.modules, key=lambda x: x["order"]):
                module = one_or_none(db, select(CourseModule).where(CourseModule.track_id == track.id, CourseModule.order == module_item["order"], CourseModule.title == module_item["title"]), f"module {module_item['slug']}")
                conflicting = list(db.execute(select(CourseModule).where(CourseModule.track_id == track.id, CourseModule.order == module_item["order"])).scalars().all())
                if module is None and conflicting:
                    raise ImportInputError(f"Module {module_item['slug']}: ordre déjà utilisé par un autre titre.")
                if module is None:
                    module = CourseModule(track_id=track.id, title=module_item["title"], description=module_item.get("description"), order=module_item["order"], published=False)
                    db.add(module)
                    db.flush()
                    created["modules"] += 1
                else:
                    reused["modules"] += 1
                module_by_slug[module_item["slug"]] = module
            for lesson_plan in sorted(plan.lessons, key=lambda x: (x.item["module"], x.item["order"])):
                module = module_by_slug[lesson_plan.item["module"]]
                lesson = one_or_none(db, select(Lesson).where(Lesson.module_id == module.id, Lesson.order == lesson_plan.item["order"], Lesson.title == lesson_plan.item["title"]), f"leçon {lesson_plan.item['slug']}")
                conflicting = list(db.execute(select(Lesson).where(Lesson.module_id == module.id, Lesson.order == lesson_plan.item["order"])).scalars().all())
                if lesson is None and conflicting:
                    raise ImportInputError(f"Leçon {lesson_plan.item['slug']}: ordre déjà utilisé par un autre titre.")
                if lesson is None:
                    lesson = Lesson(module_id=module.id, title=lesson_plan.item["title"], content=lesson_plan.content, duration_minutes=lesson_plan.item["duration_minutes"], order=lesson_plan.item["order"], published=False)
                    db.add(lesson)
                    db.flush()
                    created["lessons"] += 1
                else:
                    reused["lessons"] += 1
                    if lesson.content and lesson_plan.source_sha256 not in lesson.content:
                        raise ImportInputError(f"Leçon {lesson_plan.item['slug']}: contenu existant différent; aucune écriture destructive.")
                quiz = one_or_none(db, select(Quiz).where(Quiz.lesson_id == lesson.id), f"quiz {lesson_plan.item['slug']}")
                if quiz is None:
                    quiz = Quiz(lesson_id=lesson.id, title=lesson_plan.quiz["title"], passing_score=lesson_plan.quiz["passing_score"])
                    for question_item in lesson_plan.quiz["questions"]:
                        question = Question(question=question_item["question"], type=question_item["type"])
                        for answer_item in question_item["answers"]:
                            question.answers.append(Answer(answer=answer_item["answer"], correct=answer_item["correct"]))
                            created["answers"] += 1
                        quiz.questions.append(question)
                        created["questions"] += 1
                    db.add(quiz)
                    db.flush()
                    created["quizzes"] += 1
                else:
                    reused["quizzes"] += 1
        return {"mode": "apply", "writes_performed": True, "status": "applied", "created": created, "reused": reused}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> int:
    args = parse_args()
    mode = "apply" if args.apply else "dry-run"
    try:
        plan = build_plan(args)
        if args.apply:
            result = apply_plan(plan)
        else:
            result = dry_run_payload(plan, args.max_details)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ImportInputError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"mode": mode, "writes_performed": False, "status": "blocked", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"mode": mode, "writes_performed": False, "status": "failed", "error_type": type(exc).__name__, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
