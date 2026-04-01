"""002 tenancy tables — shards, tenants, quota_events.

Revision ID: 002_tenancy_tables
Revises: 001_auth_tables
Create Date: 2026-04-01
"""
from __future__ import annotations
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

revision = "002_tenancy_tables"
down_revision = "001_auth_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enums
    op.execute(
        "CREATE TYPE platform.tenant_type AS ENUM "
        "('SCHOOL','COLLEGE','COACHING','GROUP')"
    )
    op.execute(
        "CREATE TYPE platform.tenant_status AS ENUM "
        "('PROVISIONING','ACTIVE','WARNING','SUSPENDED','TERMINATED','ARCHIVED')"
    )
    op.execute(
        "CREATE TYPE platform.tenant_plan AS ENUM "
        "('STARTER','GROWTH','SCALE','ENTERPRISE')"
    )
    op.execute(
        "CREATE TYPE platform.institution_board AS ENUM "
        "('CBSE','ICSE','STATE','IB','IGCSE','NA')"
    )
    op.execute(
        "CREATE TYPE platform.quota_event_type AS ENUM "
        "('STUDENT_ADDED','STUDENT_REMOVED','STAFF_ADDED','STAFF_REMOVED',"
        "'PLAN_UPGRADED','PLAN_DOWNGRADED','SOFT_LIMIT_WARNING',"
        "'HARD_LIMIT_REACHED','STORAGE_WARNING','STORAGE_FULL')"
    )

    # shards
    op.create_table(
        "shards",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("db_url_encrypted", sa.String(512), nullable=False),
        sa.Column("region", sa.String(32), nullable=False, server_default="ap-south-1"),
        sa.Column("max_tenants", sa.Integer, nullable=False, server_default="500"),
        sa.Column("current_tenants", sa.Integer, nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        schema="platform",
    )

    # Seed Phase 1 shard (will be updated by admin with real db_url)
    op.execute(
        "INSERT INTO platform.shards (id, db_url_encrypted, region) "
        "VALUES ('shard-001', 'REPLACE_ME', 'ap-south-1')"
    )

    # tenants
    op.create_table(
        "tenants",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("uid", sa.String(26), nullable=False, unique=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(80), nullable=False, unique=True),
        sa.Column("tenant_type",
                  sa.Enum("SCHOOL","COLLEGE","COACHING","GROUP",
                          name="tenant_type", schema="platform"), nullable=False),
        sa.Column("shard_id", sa.String(32),
                  sa.ForeignKey("platform.shards.id"), nullable=False),
        sa.Column("status",
                  sa.Enum("PROVISIONING","ACTIVE","WARNING","SUSPENDED","TERMINATED","ARCHIVED",
                          name="tenant_status", schema="platform"),
                  nullable=False, server_default="PROVISIONING"),
        sa.Column("plan",
                  sa.Enum("STARTER","GROWTH","SCALE","ENTERPRISE",
                          name="tenant_plan", schema="platform"),
                  nullable=False, server_default="STARTER"),
        sa.Column("max_students", sa.Integer, nullable=False, server_default="500"),
        sa.Column("max_staff", sa.Integer, nullable=False, server_default="50"),
        sa.Column("storage_gb", sa.Integer, nullable=False, server_default="5"),
        sa.Column("current_students", sa.Integer, nullable=False, server_default="0"),
        sa.Column("current_staff", sa.Integer, nullable=False, server_default="0"),
        sa.Column("storage_used_mb", sa.BigInteger, nullable=False, server_default="0"),
        sa.Column("custom_domain", sa.String(253), nullable=True, unique=True),
        sa.Column("logo_url", sa.String(512), nullable=True),
        sa.Column("primary_color", sa.String(7), nullable=False, server_default="#1B4F72"),
        sa.Column("secondary_color", sa.String(7), nullable=False, server_default="#2E86C1"),
        sa.Column("font_family", sa.String(64), nullable=False, server_default="Inter"),
        sa.Column("homepage_layout", JSON, nullable=True),
        sa.Column("board",
                  sa.Enum("CBSE","ICSE","STATE","IB","IGCSE","NA",
                          name="institution_board", schema="platform"),
                  nullable=False, server_default="NA"),
        sa.Column("udise_code", sa.String(11), nullable=True),
        sa.Column("gst_number", sa.String(15), nullable=True),
        sa.Column("academic_year_start_month", sa.Integer, nullable=False, server_default="6"),
        sa.Column("enabled_modules", JSON, nullable=True),
        sa.Column("whatsapp_enabled", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("whatsapp_wallet_paise", sa.BigInteger, nullable=False, server_default="0"),
        sa.Column("admin_name", sa.String(120), nullable=True),
        sa.Column("admin_email", sa.String(254), nullable=True),
        sa.Column("admin_mobile", sa.String(10), nullable=True),
        sa.Column("suspended_at", sa.String(30), nullable=True),
        sa.Column("terminated_at", sa.String(30), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        schema="platform",
    )
    op.create_index("ix_platform_tenants_uid", "tenants", ["uid"], schema="platform")
    op.create_index("ix_platform_tenants_slug", "tenants", ["slug"], schema="platform")

    # tenant_quota_events
    op.create_table(
        "tenant_quota_events",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.BigInteger,
                  sa.ForeignKey("platform.tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_type",
                  sa.Enum("STUDENT_ADDED","STUDENT_REMOVED","STAFF_ADDED","STAFF_REMOVED",
                          "PLAN_UPGRADED","PLAN_DOWNGRADED","SOFT_LIMIT_WARNING",
                          "HARD_LIMIT_REACHED","STORAGE_WARNING","STORAGE_FULL",
                          name="quota_event_type", schema="platform"),
                  nullable=False),
        sa.Column("old_value", sa.Integer, nullable=True),
        sa.Column("new_value", sa.Integer, nullable=True),
        sa.Column("actor_id", sa.BigInteger, nullable=True),
        sa.Column("note", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        schema="platform",
    )
    op.create_index("ix_platform_quota_events_tenant", "tenant_quota_events", ["tenant_id"], schema="platform")

    # PostgreSQL RLS on tenants is NOT applied here (tenants table is central registry,
    # not a per-tenant table). RLS is applied in per-shard migrations (003+).


def downgrade() -> None:
    for t in ["tenant_quota_events", "tenants", "shards"]:
        op.drop_table(t, schema="platform")
    for e in ["quota_event_type", "institution_board", "tenant_plan",
              "tenant_status", "tenant_type"]:
        op.execute(f"DROP TYPE IF EXISTS platform.{e}")
