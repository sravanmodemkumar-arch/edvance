"""001 auth tables — users, sessions, OTPs.

Revision ID: 001_auth_tables
Revises:
Create Date: 2026-04-01
"""
from __future__ import annotations
from alembic import op
import sqlalchemy as sa

revision = "001_auth_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create platform schema
    op.execute("CREATE SCHEMA IF NOT EXISTS platform")

    # Enums
    op.execute(
        "CREATE TYPE platform.institution_type AS ENUM "
        "('SCHOOL', 'COACHING', 'HOSTEL', 'PLATFORM')"
    )
    op.execute(
        "CREATE TYPE platform.user_status AS ENUM "
        "('ACTIVE', 'DISABLED', 'PENDING_VERIFICATION')"
    )
    op.execute(
        "CREATE TYPE platform.otp_purpose AS ENUM "
        "('FORGOT_PASSWORD', 'ACCOUNT_DELETE', 'CHANGE_PHONE', 'CHANGE_EMAIL', "
        "'HIGH_VALUE_PAYMENT', 'DSAR', 'DEACTIVATE_INSTITUTION')"
    )

    # users
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("uid", sa.String(26), nullable=False, unique=True),
        sa.Column("email", sa.String(254), nullable=True, unique=True),
        sa.Column("mobile", sa.String(10), nullable=True, unique=True),
        sa.Column("password_hash", sa.String(128), nullable=True),
        sa.Column("full_name", sa.String(120), nullable=False),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "DISABLED", "PENDING_VERIFICATION",
                    name="user_status", schema="platform"),
            nullable=False,
            server_default="ACTIVE",
        ),
        sa.Column("failed_attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        schema="platform",
    )
    op.create_index("ix_platform_users_uid", "users", ["uid"], schema="platform")
    op.create_index("ix_platform_users_email", "users", ["email"], schema="platform")
    op.create_index("ix_platform_users_mobile", "users", ["mobile"], schema="platform")

    # user_tenants
    op.create_table(
        "user_tenants",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tenant_id", sa.Integer, nullable=False),
        sa.Column(
            "institution_type",
            sa.Enum("SCHOOL", "COACHING", "HOSTEL", "PLATFORM",
                    name="institution_type", schema="platform"),
            nullable=False,
        ),
        sa.Column("roles", sa.String(512), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.UniqueConstraint("user_id", "tenant_id", name="uq_user_tenant"),
        schema="platform",
    )
    op.create_index("ix_platform_user_tenants_user_id", "user_tenants", ["user_id"], schema="platform")
    op.create_index("ix_platform_user_tenants_tenant_id", "user_tenants", ["tenant_id"], schema="platform")

    # sessions
    op.create_table(
        "sessions",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("uid", sa.String(26), nullable=False, unique=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tenant_id", sa.BigInteger, nullable=False),
        sa.Column("refresh_token_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("family_id", sa.String(36), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        schema="platform",
    )
    op.create_index("ix_platform_sessions_user_id", "sessions", ["user_id"], schema="platform")
    op.create_index("ix_platform_sessions_family_id", "sessions", ["family_id"], schema="platform")

    # password_reset_tokens
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        schema="platform",
    )
    op.create_index("ix_platform_prt_user_id", "password_reset_tokens", ["user_id"], schema="platform")

    # otps
    op.create_table(
        "otps",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger, nullable=False),
        sa.Column(
            "purpose",
            sa.Enum("FORGOT_PASSWORD", "ACCOUNT_DELETE", "CHANGE_PHONE", "CHANGE_EMAIL",
                    "HIGH_VALUE_PAYMENT", "DSAR", "DEACTIVATE_INSTITUTION",
                    name="otp_purpose", schema="platform"),
            nullable=False,
        ),
        sa.Column("otp_hash", sa.String(128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("verified", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        schema="platform",
    )
    op.create_index("ix_platform_otps_user_id", "otps", ["user_id"], schema="platform")

    # otp_rate_limits
    op.create_table(
        "otp_rate_limits",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("identifier", sa.String(254), nullable=False),
        sa.Column(
            "purpose",
            sa.Enum("FORGOT_PASSWORD", "ACCOUNT_DELETE", "CHANGE_PHONE", "CHANGE_EMAIL",
                    "HIGH_VALUE_PAYMENT", "DSAR", "DEACTIVATE_INSTITUTION",
                    name="otp_purpose", schema="platform", create_type=False),
            nullable=False,
        ),
        sa.Column("count", sa.Integer, nullable=False, server_default="1"),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        schema="platform",
    )
    op.create_index("ix_platform_otp_rate_limits_identifier", "otp_rate_limits", ["identifier"], schema="platform")

    # audit_logs
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("table_name", sa.String(64), nullable=False),
        sa.Column("record_id", sa.BigInteger, nullable=False),
        sa.Column("action", sa.String(16), nullable=False),
        sa.Column("actor_id", sa.BigInteger, nullable=True),
        sa.Column("tenant_id", sa.Integer, nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(512), nullable=True),
        sa.Column("changed_fields", sa.Text, nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        schema="platform",
    )
    op.create_index("ix_audit_table_record", "audit_logs", ["table_name", "record_id"], schema="platform")
    op.create_index("ix_audit_actor", "audit_logs", ["actor_id"], schema="platform")
    op.create_index("ix_audit_tenant", "audit_logs", ["tenant_id"], schema="platform")

    # Alembic version table in platform schema
    op.execute("CREATE TABLE IF NOT EXISTS platform.alembic_version (version_num VARCHAR(32) NOT NULL)")


def downgrade() -> None:
    for table in [
        "audit_logs", "otp_rate_limits", "otps",
        "password_reset_tokens", "sessions", "user_tenants", "users",
    ]:
        op.drop_table(table, schema="platform")
    op.execute("DROP TYPE IF EXISTS platform.otp_purpose")
    op.execute("DROP TYPE IF EXISTS platform.user_status")
    op.execute("DROP TYPE IF EXISTS platform.institution_type")
    op.execute("DROP SCHEMA IF EXISTS platform CASCADE")
