"""add last few column to post table

Revision ID: a5595bba18f7
Revises: ee259422086d
Create Date: 2022-05-03 02:43:23.508253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5595bba18f7'
down_revision = 'ee259422086d'
branch_labels = None
depends_on = None


def upgrade():
  op.add_column('posts', sa.Column(
      'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
  op.add_column('posts', sa.Column('rating', sa.Integer(), nullable=True),)
  op.add_column('posts', sa.Column(
      'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
  pass


def downgrade():
  pass
