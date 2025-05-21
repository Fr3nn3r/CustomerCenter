"""fix duplicate campaign_id in leads table

Revision ID: 0004
Revises: 0003
Create Date: 2024-03-19

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # First, let's check if there are any duplicate columns
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = inspector.get_columns("leads")
    campaign_id_columns = [
        col["name"] for col in columns if col["name"] == "campaign_id"
    ]

    if len(campaign_id_columns) > 1:
        # If we have duplicate columns, drop the table and recreate it
        op.drop_table("leads")

        # Recreate the leads table with a single campaign_id
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
    # No downgrade needed as this is a fix for a corrupted state
    pass
