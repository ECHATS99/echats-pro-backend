"""Peuple la base avec les données indispensables au fonctionnement du backend :
rôles RBAC de base, permissions Phase 1, et plans d'abonnement (GO/CORE_I/PARABEN/CHAMBRE_CLOSE).

Ce script est un PRÉ-REQUIS : sans lui, l'auto-provisioning au premier login Firebase
(modules/auth/repository.create_user_from_firebase) échoue car le rôle 'student' et le
plan 'GO' n'existeraient pas encore en base.

Usage : python -m scripts.seed
"""
from app.core.database import SessionLocal
from app.core.constants import RoleName, PlanCode
from app.core import permissions as perm_const
from app.models.plan import Plan
from app.models.role_permission import Permission, Role

# Permissions Phase 1
BASE_PERMISSIONS = [
    ("users.read", "users", "Lire les profils utilisateurs"),
    ("users.update", "users", "Modifier un profil utilisateur"),
    ("users.delete", "users", "Supprimer un utilisateur"),
    ("admin.access", "admin", "Accéder au panel d'administration"),
    # Permissions Phase 2 (voir app/core/permissions.py pour la liste canonique)
    (perm_const.TRACKS_CREATE, "tracks", "Créer un track"),
    (perm_const.TRACKS_UPDATE, "tracks", "Modifier un track/module/leçon/exercice"),
    (perm_const.TRACKS_DELETE, "tracks", "Supprimer un track/module/leçon/exercice"),
    (perm_const.CTF_PLAY, "ctf", "Participer aux challenges CTF"),
    (perm_const.CTF_CREATE, "ctf", "Créer/modifier un challenge CTF"),
    (perm_const.PAYMENTS_READ, "payments", "Consulter l'historique des paiements"),
    (perm_const.PAYMENTS_MANAGE, "payments", "Gérer les commandes et abonnements"),
    (perm_const.PAYMENTS_REFUND, "payments", "Effectuer un remboursement"),
    (perm_const.PRODUCTS_CREATE, "products", "Gérer la boutique BLACKHAWK LAB"),
    (perm_const.ANALYTICS_READ, "analytics", "Consulter les tableaux de bord analytics"),
    (perm_const.NOTIFICATIONS_SEND, "notifications", "Diffuser une notification en masse"),
    (perm_const.PARABEN_MANAGE, "paraben", "Gérer les cours et revenus Paraben"),
    (perm_const.INSTITUTION_MANAGE, "institution", "Gérer les institutions (Chambre Close)"),
    (perm_const.CLASSROOM_CREATE, "classroom", "Créer une Classroom"),
    (perm_const.IA_MANAGE, "ia", "Modifier les prompts système IA"),
]

# Rôle -> liste de noms de permissions.
ROLE_PERMISSIONS = {
    RoleName.STUDENT.value: [perm_const.CTF_PLAY, perm_const.CLASSROOM_CREATE],
    RoleName.PREMIUM.value: [perm_const.CTF_PLAY, perm_const.CLASSROOM_CREATE],
    RoleName.MENTOR.value: ["users.read", perm_const.CTF_PLAY],
    RoleName.INSTRUCTOR.value: ["users.read", perm_const.CLASSROOM_CREATE, perm_const.TRACKS_CREATE, perm_const.TRACKS_UPDATE],
    RoleName.INSTITUTION_MANAGER.value: ["users.read", "users.update", perm_const.INSTITUTION_MANAGE, perm_const.ANALYTICS_READ],
    RoleName.PARABEN_MANAGER.value: ["users.read", perm_const.PARABEN_MANAGE, perm_const.ANALYTICS_READ],
    RoleName.ADMIN.value: [
        "users.read", "users.update", "users.delete", "admin.access",
        perm_const.TRACKS_CREATE, perm_const.TRACKS_UPDATE, perm_const.TRACKS_DELETE,
        perm_const.CTF_CREATE, perm_const.PAYMENTS_READ, perm_const.PAYMENTS_MANAGE,
        perm_const.PAYMENTS_REFUND, perm_const.PRODUCTS_CREATE, perm_const.ANALYTICS_READ,
        perm_const.NOTIFICATIONS_SEND, perm_const.PARABEN_MANAGE, perm_const.INSTITUTION_MANAGE,
        perm_const.IA_MANAGE,
    ],
    RoleName.SUPER_ADMIN.value: [name for name, _, _ in BASE_PERMISSIONS],
}

DEFAULT_PLANS = [
    {"code": PlanCode.GO.value, "name": "GO", "price": 0, "currency": "XAF",
     "duration_days": None, "max_ai_requests_per_day": 10, "max_storage_mb": 100},
    {"code": PlanCode.CORE_I.value, "name": "CORE I", "price": 15000, "currency": "XAF",
     "duration_days": 30, "max_ai_requests_per_day": 200, "max_storage_mb": 2000},
    {"code": PlanCode.PARABEN_NIVEAU_1.value, "name": "Paraben Niveau 1", "price": 25000,
     "currency": "XAF", "duration_days": 30, "max_ai_requests_per_day": 200, "max_storage_mb": 2000},
    {"code": PlanCode.CHAMBRE_CLOSE.value, "name": "Chambre Close (Institutionnel)", "price": 0,
     "currency": "XAF", "duration_days": 365, "max_ai_requests_per_day": 500, "max_storage_mb": 10000},
]


def seed_permissions(db) -> dict[str, Permission]:
    existing = {p.name: p for p in db.query(Permission).all()}
    for name, module, description in BASE_PERMISSIONS:
        if name not in existing:
            perm = Permission(name=name, module=module, description=description)
            db.add(perm)
            existing[name] = perm
    db.commit()
    return existing


def seed_roles(db, permissions: dict[str, Permission]) -> None:
    existing = {r.name: r for r in db.query(Role).all()}
    for role_name, perm_names in ROLE_PERMISSIONS.items():
        role = existing.get(role_name)
        if role is None:
            role = Role(name=role_name)
            db.add(role)
            db.flush()
            existing[role_name] = role
        role.permissions = [permissions[name] for name in perm_names if name in permissions]
    db.commit()


def seed_plans(db) -> None:
    existing_codes = {p.code for p in db.query(Plan).all()}
    for plan_data in DEFAULT_PLANS:
        if plan_data["code"] not in existing_codes:
            db.add(Plan(**plan_data))
    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        permissions = seed_permissions(db)
        seed_roles(db, permissions)
        seed_plans(db)
        print("Seed terminé : rôles, permissions et plans de base créés.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
