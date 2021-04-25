"""create_tables_test

Revision ID: b4b37850de38
Revises: 5f7fc09a9d48
Create Date: 2021-04-25 15:13:36.540172

"""

from alembic import op 
import sqlalchemy as sa


# revision identifiers, used by alembic
revision = 'b4b37850de38'
down_revision = '5f7fc09a9d48'
branch_labels = None
depends_on = None

def create_table() -> None:
    op.create_table(
        "footprints",
        sa.Column("id", sa.Integer, primary_key = True),
        sa.Column("category", sa.Text, nullable = False),
        sa.Column("subcategory", sa.Text, nullable = False, index = True),
        sa.Column("item", sa.Text, nullable = False),
        sa.Column("footprint", sa.Numeric(10,2), nullable = False),
    )


def upgrade() -> None:
    create_table()
    

def downgrade() -> None:
    op.drop_table("footprints")