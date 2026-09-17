"""Phase 1 : socle Auth / RBAC / Abonnements / Institutions / Audit

Revision ID: 0001_phase1_core_auth
Revises:
Create Date: 2026-07-28

NOTE DE TRANSPARENCE : cette migration ne couvre que les tables implémentées en Phase 1
(institutions, roles, permissions, role_permissions, users, user_roles, plans,
subscriptions, audit_logs). Les ~40 autres tables du SRS (tracks, ctf, payments, labs,
classroom, etc.) seront ajoutées par des migrations dédiées au fur et à mesure de
l'implémentation domaine par domaine, sans modifier cette migration existante.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_phase1_core_auth"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "institutions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("country", sa.String(2)),
        sa.Column("type", sa.String(50)),
        sa.Column("contact_email", sa.String(255)),
        sa.Column("max_users", sa.Integer, server_default="50"),
        sa.Column("paraben_access", sa.Boolean, server_default=sa.false()),
        sa.Column("chamber_close_enabled", sa.Boolean, server_default=sa.true()),
        sa.Column("active", sa.Boolean, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False, unique=True),
        sa.Column("description", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "permissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("module", sa.String(50)),
        sa.Column("description", sa.String(255)),
    )

    op.create_table(
        "role_permissions",
        sa.Column("role_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("permission_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("firebase_uid", sa.String(128), nullable=False, unique=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True),
        sa.Column("avatar_url", sa.String(500)),
        sa.Column("country", sa.String(2)),
        sa.Column("city", sa.String(100)),
        sa.Column("language", sa.String(5), server_default="fr"),
        sa.Column("timezone", sa.String(50), server_default="Africa/Brazzaville"),
        sa.Column("bio", sa.String(1000)),
        sa.Column("xp", sa.Integer, server_default="0"),
        sa.Column("level", sa.Integer, server_default="1"),
        sa.Column("streak", sa.Integer, server_default="0"),
        sa.Column("status", sa.String(30), server_default="active"),
        sa.Column("totp_secret_encrypted", sa.String(500)),
        sa.Column("totp_enabled", sa.Boolean, server_default=sa.false()),
        sa.Column("institution_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("institutions.id", ondelete="SET NULL")),
        sa.Column("last_login", sa.DateTime(timezone=True)),
        sa.Column("last_login_ip", sa.String(45)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_users_firebase_uid", "users", ["firebase_uid"])
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_username", "users", ["username"])

    op.create_table(
        "user_roles",
        sa.Column("user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("role_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), server_default="0"),
        sa.Column("currency", sa.String(3), server_default="XAF"),
        sa.Column("duration_days", sa.Integer),
        sa.Column("features", postgresql.JSON, server_default="{}"),
        sa.Column("max_ai_requests_per_day", sa.Integer, server_default="10"),
        sa.Column("max_storage_mb", sa.Integer, server_default="100"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("plan_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("plans.id"), nullable=False),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("payment_provider", sa.String(20)),
        sa.Column("starts_at", sa.DateTime(timezone=True)),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
        sa.Column("renewal", sa.Boolean, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("role", sa.String(50)),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("module", sa.String(50)),
        sa.Column("resource", sa.String(100)),
        sa.Column("resource_id", sa.String(100)),
        sa.Column("old_value", postgresql.JSON),
        sa.Column("new_value", postgresql.JSON),
        sa.Column("ip_address", postgresql.INET),
        sa.Column("user_agent", sa.String(500)),
        sa.Column("country", sa.String(2)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_audit_logs_created_at", "audit_logs", ["created_at"])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("subscriptions")
    op.drop_table("plans")
    op.drop_table("user_roles")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_firebase_uid", table_name="users")
    op.drop_table("users")
    op.drop_table("role_permissions")
    op.drop_table("permissions")
    op.drop_table("roles")
    op.drop_table("institutions")
