"""empty message

Revision ID: b2d4bf659a60
Revises: 3fed8757f20f
Create Date: 2021-01-14 13:29:41.845206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2d4bf659a60'
down_revision = '3fed8757f20f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('size', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('file', 'size')
    # ### end Alembic commands ###