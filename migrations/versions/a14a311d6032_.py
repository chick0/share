"""empty message

Revision ID: a14a311d6032
Revises: 
Create Date: 2021-01-28 00:07:59.098028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a14a311d6032'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('idx', sa.String(length=36), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('upload', sa.DateTime(), nullable=False),
    sa.Column('md5', sa.String(length=32), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('idx'),
    sa.UniqueConstraint('idx')
    )
    op.create_table('report',
    sa.Column('md5', sa.String(length=32), nullable=False),
    sa.Column('upload', sa.DateTime(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('ban', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('md5'),
    sa.UniqueConstraint('md5')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('report')
    op.drop_table('file')
    # ### end Alembic commands ###