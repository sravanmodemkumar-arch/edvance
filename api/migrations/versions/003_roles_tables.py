"""003 roles tables — roles, role_assignments, role_delegations, role_change_log.

Revision ID: 003_roles_tables
Revises: 002_tenancy_tables
Create Date: 2026-04-01
"""
from __future__ import annotations
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

revision = "003_roles_tables"
down_revision = "002_tenancy_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "CREATE TYPE platform.role_group AS ENUM "
        "('PLATFORM','GROUP','SCHOOL','COLLEGE','COACHING','EXAM_DOMAIN','TSP','PARENT','B2B','STUDENT','ALUMNI')"
    )

    # roles
    op.create_table(
        "roles",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("code", sa.String(40), nullable=False),
        sa.Column("role_group",
                  sa.Enum("PLATFORM","GROUP","SCHOOL","COLLEGE","COACHING",
                          "EXAM_DOMAIN","TSP","PARENT","B2B","STUDENT","ALUMNI",
                          name="role_group", schema="platform"),
                  nullable=False),
        sa.Column("hierarchy_level", sa.Integer, nullable=False, server_default="50"),
        sa.Column("is_system", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("permissions", JSON, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("approved_by", sa.BigInteger, nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        schema="platform",
    )
    op.create_index("ix_platform_roles_tenant_id", "roles", ["tenant_id"], schema="platform")
    op.create_index("ix_platform_roles_code", "roles", ["code"], schema="platform")

    # role_assignments
    op.create_table(
        "role_assignments",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.Integer, nullable=False),
        sa.Column("user_id", sa.BigInteger, nullable=False),
        sa.Column("role_id", sa.BigInteger, sa.ForeignKey("platform.roles.id"), nullable=False),
        sa.Column("role_code", sa.String(40), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("assigned_by_id", sa.BigInteger, nullable=False),
        sa.Column("scope_context", JSON, nullable=True),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        schema="platform",
    )
    op.create_index("ix_platform_ra_user_tenant", "role_assignments",
                    ["user_id", "tenant_id"], schema="platform")

    # role_delegations
    op.create_table(
        "role_delegations",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.Integer, nullable=False),
        sa.Column("delegator_user_id", sa.BigInteger, nullable=False),
        sa.Column("delegate_user_id", sa.BigInteger, nullable=False),
        sa.Column("role_code", sa.String(40), nullable=False),
        sa.Column("permissions", JSON, nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("reason", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        schema="platform",
    )
    op.create_index("ix_platform_rd_delegate", "role_delegations",
                    ["delegate_user_id", "tenant_id"], schema="platform")

    # role_change_log
    op.create_table(
        "role_change_log",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.Integer, nullable=False),
        sa.Column("target_user_id", sa.BigInteger, nullable=False),
        sa.Column("changed_by_id", sa.BigInteger, nullable=False),
        sa.Column("action", sa.String(20), nullable=False),
        sa.Column("role_code", sa.String(40), nullable=False),
        sa.Column("previous_state", JSON, nullable=True),
        sa.Column("new_state", JSON, nullable=True),
        sa.Column("reason", sa.String(255), nullable=True),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        schema="platform",
    )
    op.create_index("ix_platform_rcl_tenant_user", "role_change_log",
                    ["tenant_id", "target_user_id"], schema="platform")


def downgrade() -> None:
    for t in ["role_change_log", "role_delegations", "role_assignments", "roles"]:
        op.drop_table(t, schema="platform")
    op.execute("DROP TYPE IF EXISTS platform.role_group")
