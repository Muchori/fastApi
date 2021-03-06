"""add phone number

Revision ID: 895c5b18241a
Revises: 7295621774f6
Create Date: 2022-05-03 03:00:38.621660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '895c5b18241a'
down_revision = '7295621774f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone')
    # ### end Alembic commands ###
