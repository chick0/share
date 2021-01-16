"""empty message

Revision ID: 5884859ca373
Revises: 5d1f7d5a6aab
Create Date: 2021-01-16 09:18:52.825804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5884859ca373'
down_revision = '5d1f7d5a6aab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('report', sa.Column('ban', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('report', 'ban')
    # ### end Alembic commands ###