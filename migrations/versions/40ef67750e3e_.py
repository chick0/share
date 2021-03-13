"""empty message

Revision ID: 40ef67750e3e
Revises: a7952c245ac1
Create Date: 2021-03-13 21:01:51.228243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40ef67750e3e'
down_revision = 'a7952c245ac1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('password', sa.String(length=96), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('file', 'password')
    # ### end Alembic commands ###
