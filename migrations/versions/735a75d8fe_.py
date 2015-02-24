""" Add click table

Revision ID: 735a75d8fe
Revises: 7e095801da
Create Date: 2015-02-24 13:58:27.831915

"""

# revision identifiers, used by Alembic.
revision = '735a75d8fe'
down_revision = '7e095801da'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('click',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('clicked_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('click')
    ### end Alembic commands ###