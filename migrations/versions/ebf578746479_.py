"""empty message

Revision ID: ebf578746479
Revises: a14a311d6032
Create Date: 2021-02-06 03:39:52.882699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebf578746479'
down_revision = 'a14a311d6032'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('email', sa.String(length=96), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('file', 'email')
    # ### end Alembic commands ###
