"""create post table

Revision ID: fe13f6e5d6cb
Revises: 
Create Date: 2022-05-03 01:51:35.794273

"""
from tokenize import String
from alembic import op
import sqlalchemy as sa

import uuid


# revision identifiers, used by Alembic.
revision = 'fe13f6e5d6cb'
down_revision = None
branch_labels = None
depends_on = None


#generating unique uuid function
def generate_uuid():
  return str(uuid.uuid4())

def upgrade():
  op.create_table('posts', 
  sa.Column('id', sa.String(), nullable=False, primary_key=True, default = generate_uuid),
  sa.Column('title', sa.String(), nullable=False ))
  pass


def downgrade():
  op.drop_table('posts')
  pass
