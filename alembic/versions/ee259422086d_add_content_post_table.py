"""add content post table

Revision ID: ee259422086d
Revises: 367dcb23f823
Create Date: 2022-05-03 02:32:56.381273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee259422086d'
down_revision = '367dcb23f823'
branch_labels = None
depends_on = None


def upgrade():
  op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
  pass


def downgrade():
  op.drop_column('posts', 'content')
  pass
