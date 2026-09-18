"""Chambre Close : extension institutions + table access_keys

Revision ID: 0005_chambre_close
Revises: 0004_ctf_terminal_commands
Create Date: 2026-09-18
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0005_chambre_close"
down_revision = "0004_ctf_terminal_commands"
branch_labels = None
depends_on = None


def upgrade():
    # ============================================================
    # 1. Étendre la table institutions (idempotent)
    # ============================================================
    op.execute("""
        ALTER TABLE institutions
        ADD COLUMN IF NOT EXISTS code VARCHAR(30) UNIQUE,
        ADD COLUMN IF NOT EXISTS slug VARCHAR(100) UNIQUE,
        ADD COLUMN IF NOT EXISTS prefix VARCHAR(10),
        ADD COLUMN IF NOT EXISTS tagline VARCHAR(300),
        ADD COLUMN IF NOT EXISTS description TEXT,
        ADD COLUMN IF NOT EXISTS logo VARCHAR(500),
        ADD COLUMN IF NOT EXISTS cover_image VARCHAR(500),
        ADD COLUMN IF NOT EXISTS accent_color VARCHAR(20) DEFAULT '#CCFF00',
        ADD COLUMN IF NOT EXISTS owner_uid VARCHAR(100),
        ADD COLUMN IF NOT EXISTS owner_name VARCHAR(200),
        ADD COLUMN IF NOT EXISTS is_private BOOLEAN DEFAULT FALSE,
        ADD COLUMN IF NOT EXISTS is_public BOOLEAN DEFAULT TRUE,
        ADD COLUMN IF NOT EXISTS requires_key BOOLEAN DEFAULT FALSE,
        ADD COLUMN IF NOT EXISTS members_count INTEGER DEFAULT 0,
        ADD COLUMN IF NOT EXISTS visitors_count INTEGER DEFAULT 0
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_institutions_code ON institutions(code)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_institutions_slug ON institutions(slug)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_institutions_owner ON institutions(owner_uid)")

    # ============================================================
    # 2. Table institution_access_keys
    # ============================================================
    op.create_table(
        "institution_access_keys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("institution_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("key", sa.String(32), unique=True, nullable=False),
        sa.Column("assigned_role", sa.String(50), nullable=False, server_default="ELEVE"),
        sa.Column("max_uses", sa.Integer, nullable=False, server_default="20"),
        sa.Column("current_uses", sa.Integer, nullable=False, server_default="0"),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
        sa.Column("created_by", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_inst_access_keys_key", "institution_access_keys", ["key"])
    op.create_index("ix_inst_access_keys_inst", "institution_access_keys", ["institution_id"])


def downgrade():
    op.drop_table("institution_access_keys")
    op.execute("""
        ALTER TABLE institutions
        DROP COLUMN IF EXISTS code,
        DROP COLUMN IF EXISTS slug,
        DROP COLUMN IF EXISTS prefix,
        DROP COLUMN IF EXISTS tagline,
        DROP COLUMN IF EXISTS description,
        DROP COLUMN IF EXISTS logo,
        DROP COLUMN IF EXISTS cover_image,
        DROP COLUMN IF EXISTS accent_color,
        DROP COLUMN IF EXISTS owner_uid,
        DROP COLUMN IF EXISTS owner_name,
        DROP COLUMN IF EXISTS is_private,
        DROP COLUMN IF EXISTS is_public,
        DROP COLUMN IF EXISTS requires_key,
        DROP COLUMN IF EXISTS members_count,
        DROP COLUMN IF EXISTS visitors_count
    """)
