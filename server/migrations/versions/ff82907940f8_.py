"""empty message

Revision ID: ff82907940f8
Revises: 
Create Date: 2020-05-08 20:07:09.284253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff82907940f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('house',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hsetype', sa.String(length=1), nullable=True),
    sa.Column('rooms', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('method', sa.String(length=2), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('suburb', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('postcode', sa.String(length=4), nullable=True),
    sa.Column('property_count', sa.Integer(), nullable=True),
    sa.Column('distance', sa.Float(), nullable=True),
    sa.Column('house_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['house_id'], ['house.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('location')
    op.drop_table('house')
    # ### end Alembic commands ###
