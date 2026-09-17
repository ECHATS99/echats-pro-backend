"""Constantes de permissions (Partie 4.8 du SRS). Chaque permission est indépendante des
rôles ; les rôles ne sont que des groupes de permissions (Partie 8.9 du SRS). Cette liste
sert de référence unique pour scripts/seed.py et pour les dependencies require_permission(...)
utilisées dans les routes, évitant les chaînes de caractères magiques dispersées dans le code.
"""

TRACKS_CREATE = "tracks.create"
TRACKS_UPDATE = "tracks.update"
TRACKS_DELETE = "tracks.delete"

CTF_PLAY = "ctf.play"
CTF_CREATE = "ctf.create"

PAYMENTS_READ = "payments.read"
PAYMENTS_MANAGE = "payments.manage"
PAYMENTS_REFUND = "payments.refund"

USERS_UPDATE = "users.update"
USERS_DELETE = "users.delete"

PRODUCTS_CREATE = "products.create"

ANALYTICS_READ = "analytics.read"

NOTIFICATIONS_SEND = "notifications.send"

PARABEN_MANAGE = "paraben.manage"
INSTITUTION_MANAGE = "institution.manage"

CLASSROOM_CREATE = "classroom.create"

IA_MANAGE = "ia.manage"

ADMIN_ACCESS = "admin.access"

ALL_PERMISSIONS = [
    TRACKS_CREATE, TRACKS_UPDATE, TRACKS_DELETE,
    CTF_PLAY, CTF_CREATE,
    PAYMENTS_READ, PAYMENTS_MANAGE, PAYMENTS_REFUND,
    USERS_UPDATE, USERS_DELETE,
    PRODUCTS_CREATE,
    ANALYTICS_READ,
    NOTIFICATIONS_SEND,
    PARABEN_MANAGE, INSTITUTION_MANAGE,
    CLASSROOM_CREATE,
    IA_MANAGE,
    ADMIN_ACCESS,
]
