"""create_tables_test

Revision ID: b4b37850de38
Revises: 895c0bd033d5
Create Date: 2021-04-25 15:13:36.540172

"""

from alembic import op 
import sqlalchemy as sa
import os


# revision identifiers, used by alembic
revision = 'b4b37850de38'
down_revision = '895c0bd033d5'
branch_labels = None
depends_on = None

dirname = os.path.dirname(__file__)
datafile = '../../../../../data/my_records.csv'

def fill_data() -> None:
    op.execute(
        f"COPY footprints(category, subcategory, item, footprint) FROM '{datafile}' DELIMITERS ',' CSV HEADER;",
        execution_options = None
    )


def upgrade() -> None:
    fill_data()
    

def downgrade() -> None:
    op.drop_table("footprints")