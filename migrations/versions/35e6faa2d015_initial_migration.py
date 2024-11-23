"""Initial migration

Revision ID: 35e6faa2d015
Revises: f6cef474f558
Create Date: 2024-11-15 03:54:51.908829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35e6faa2d015'
down_revision = 'f6cef474f558'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('church',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('church_name', sa.String(length=100), nullable=False),
    sa.Column('contact_person', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('num_participants', sa.Integer(), nullable=False),
    sa.Column('arrival_date', sa.Date(), nullable=False),
    sa.Column('departure_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('church_name'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('church')
    # ### end Alembic commands ###
