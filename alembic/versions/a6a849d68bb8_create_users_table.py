"""create users table

Revision ID: a6a849d68bb8
Revises: fe13f6e5d6cb
Create Date: 2022-05-03 02:25:12.245575

"""
from alembic import op
import sqlalchemy as sa

import uuid


# revision identifiers, used by Alembic.
revision = 'a6a849d68bb8'
down_revision = 'fe13f6e5d6cb'
branch_labels = None
depends_on = None


#generating unique uuid function
def generate_uuid():
    return str(uuid.uuid4())

def upgrade():
  op.create_table('users',
  sa.Column('id', sa.String(), nullable=False, default = generate_uuid ),
  sa.Column('email', sa.String(), nullable=False),
  sa.Column('password', sa.String(), nullable=False),
  sa.Column('created_at', sa.TIMESTAMP(timezone=True),
      server_default=sa.text('now()'), nullable=False),
  sa.PrimaryKeyConstraint('id'),
  sa.UniqueConstraint('email'))
  pass


def downgrade():
  op.drop_table('users')
  pass
