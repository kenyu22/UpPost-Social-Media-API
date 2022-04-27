"""create posts table

Revision ID: c0bf91ae4c8f
Revises: 
Create Date: 2022-04-27 11:49:46.588300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0bf91ae4c8f'
down_revision = None
branch_labels = None
depends_on = None


# testing alembic upgrades and downgrades for database migration
def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(
    ), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_table('posts')
    pass
