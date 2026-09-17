"""Add simulated terminal commands to CTF challenges.

Revision ID: 0004_ctf_terminal_commands
Revises: 0003_merge_phase2_heads
Create Date: 2026-08-23

Existing challenges receive an empty JSONB array, so the migration does not
require backfilling application data and remains safe for non-null inserts.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0004_ctf_terminal_commands"
down_revision = "0003_merge_phase2_heads"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "ctf_challenges",
        sa.Column(
            "terminal_commands",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )
    op.add_column(
        "ctf_challenges",
        sa.Column("default_output", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("ctf_challenges", "default_output")
    op.drop_column("ctf_challenges", "terminal_commands")
