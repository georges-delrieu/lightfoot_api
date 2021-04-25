"""create_main_tables

Revision ID: 895c0bd033d5
Revises: 
Create Date: 2021-04-24 12:16:31.028671

"""

from alembic import op 
import sqlalchemy as sa


# revision identifiers, used by alembic
revision = '895c0bd033d5'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
        op.create_table(
        "footprints",
        sa.Column("id", sa.Integer, primary_key = True),
        sa.Column("category", sa.Text, nullable = False),
        sa.Column("subcategory", sa.Text, nullable = False, index = True),
        sa.Column("item", sa.Text, nullable = False),
        sa.Column("footprint", sa.Numeric(10,2), nullable = False),
    )

def downgrade() -> None:
    op.drop_table("footprints")