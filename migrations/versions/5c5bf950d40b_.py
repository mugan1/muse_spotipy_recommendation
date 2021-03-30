"""empty message

Revision ID: 5c5bf950d40b
Revises: 30dc7f6b846a
Create Date: 2021-03-30 16:06:48.423771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c5bf950d40b'
down_revision = '30dc7f6b846a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('playlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('track', sa.String(length=64), nullable=False),
    sa.Column('artist', sa.String(length=64), nullable=False),
    sa.Column('released', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recommend',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('track', sa.String(length=64), nullable=False),
    sa.Column('artist', sa.String(length=64), nullable=False),
    sa.Column('released', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recommend')
    op.drop_table('playlist')
    op.drop_table('user')
    # ### end Alembic commands ###