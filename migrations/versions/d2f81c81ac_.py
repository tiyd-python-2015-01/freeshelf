"""empty message

Revision ID: d2f81c81ac
Revises: 383397eef6b
Create Date: 2015-02-24 11:55:55.829853

"""

# revision identifiers, used by Alembic.
revision = 'd2f81c81ac'
down_revision = '383397eef6b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authorship',
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.UniqueConstraint('book_id', 'author_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('authorship')
    ### end Alembic commands ###