"""fix duplicate columns

Revision ID: 0003
Revises: 0002
Create Date: 2024-03-19

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop all existing tables
    op.drop_table("leads")
    op.drop_table("organizations")
    op.drop_table("campaigns")

    # Create campaigns table with a single campaign_id
    op.create_table(
        "campaigns",
        sa.Column(
            "campaign_id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("campaign_id"),
    )

    # Create organizations table
    op.create_table(
        "organizations",
        sa.Column(
            "organization_id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email_domain", sa.String(), nullable=False),
        sa.Column("external_id", sa.String(), nullable=True),
        sa.Column("external_source", sa.String(), nullable=True),
        sa.Column("website_url", sa.String(), nullable=True),
        sa.Column("linkedin_url", sa.String(), nullable=True),
        sa.Column("estimated_num_employees", sa.Integer(), nullable=True),
        sa.Column(
            "website_summary_data",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column(
            "website_raw_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("language", sa.String(), nullable=True),
        sa.Column("time_zone", sa.String(), nullable=True),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("formatted_organization_name", sa.String(), nullable=True),
        sa.Column("raw_address", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("organization_id"),
    )

    # Create leads table
    op.create_table(
        "leads",
        sa.Column(
            "lead_id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("campaign_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("external_id", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("headline", sa.String(), nullable=True),
        sa.Column("linkedin_url", sa.String(), nullable=True),
        sa.Column("email_verification_status", sa.String(), nullable=True),
        sa.Column("email_verification_message", sa.String(), nullable=True),
        sa.Column("email_icebreaker", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("language", sa.String(), nullable=True),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("email_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reply_received_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_contacted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["campaign_id"],
            ["campaigns.campaign_id"],
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["organizations.organization_id"],
        ),
        sa.PrimaryKeyConstraint("lead_id"),
    )
    op.create_index(op.f("ix_leads_email"), "leads", ["email"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_leads_email"), table_name="leads")
    op.drop_table("leads")
    op.drop_table("organizations")
    op.drop_table("campaigns")
