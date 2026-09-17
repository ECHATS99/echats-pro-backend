"""Fusionne les branches Phase 2 contenu et refresh sessions.

Les deux révisions 0002 ont le même parent mais couvrent des tables distinctes.
Cette révision est volontairement vide : elle sert uniquement à fournir un head
unique pour `alembic upgrade head` sur les environnements de déploiement.
"""

from alembic import op


revision = "0003_merge_phase2_heads"
down_revision = ("0002_phase2_content_ctf_commerce", "0002_refresh_sessions")
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
