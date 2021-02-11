"""empty message

Revision ID: eaffe47ed751
Revises: 4c5645ace34b
Create Date: 2021-02-11 10:54:57.683387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eaffe47ed751'
down_revision = '4c5645ace34b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('service', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('file', 'service')
    # ### end Alembic commands ###
