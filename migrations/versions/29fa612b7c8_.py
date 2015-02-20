"""empty message

Revision ID: 29fa612b7c8
Revises: 43200d49d65
Create Date: 2015-02-20 11:27:05.139240

"""

# revision identifiers, used by Alembic.
revision = '29fa612b7c8'
down_revision = '43200d49d65'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite')
    ### end Alembic commands ###
