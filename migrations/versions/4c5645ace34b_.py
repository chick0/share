"""empty message

Revision ID: 4c5645ace34b
Revises: ebf578746479
Create Date: 2021-02-06 12:27:13.596774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c5645ace34b'
down_revision = 'ebf578746479'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('delete', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('file', 'delete')
    # ### end Alembic commands ###