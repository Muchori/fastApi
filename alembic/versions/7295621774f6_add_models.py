"""add models

Revision ID: 7295621774f6
Revises: 71c0b8de2e0d
Create Date: 2022-05-03 02:56:28.996549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7295621774f6'
down_revision = '71c0b8de2e0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
