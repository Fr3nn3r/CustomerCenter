"""add linkedin_data to leads

Revision ID: 0007
Revises: 0006
Create Date: 2024-03-19

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add linkedin_data to leads in public schema
    op.add_column("leads", sa.Column("linkedin_data", sa.String(), nullable=True))

    # Add linkedin_data to leads in test schema
    op.add_column(
        "leads",
        sa.Column("linkedin_data", sa.String(), nullable=True),
        schema="test_schema",
    )


def downgrade() -> None:
    # Remove linkedin_data from leads in public schema
    op.drop_column("leads", "linkedin_data")

    # Remove linkedin_data from leads in test schema
    op.drop_column("leads", "linkedin_data", schema="test_schema")
