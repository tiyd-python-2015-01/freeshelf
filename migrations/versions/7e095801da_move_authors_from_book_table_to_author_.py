"""Move authors from book table to author table

Revision ID: 7e095801da
Revises: 2d2fd5b6584
Create Date: 2015-02-24 12:06:14.050404

"""

# revision identifiers, used by Alembic.
revision = '7e095801da'
down_revision = '2d2fd5b6584'

import re
from alembic import op
import sqlalchemy as sa



def upgrade():
    # take _authors from each book
    # split authors by commas and "and"
    # insert authors into author table if necessary
    # add book_id and author_id to authorship
    book = sa.Table('book', sa.MetaData(),
                 sa.Column('id', sa.Integer, primary_key=True),
                 sa.Column('_authors', sa.Text))
    author = sa.Table('author', sa.MetaData(),
                   sa.Column('id', sa.Integer, primary_key=True),
                   sa.Column('name', sa.String(255)))
    authorship = sa.Table('authorship', sa.MetaData(),
                       sa.Column('book_id', sa.Integer),
                       sa.Column('author_id', sa.Integer))

    conn = op.get_bind()
    result = conn.execute(book.select())
    _authors = {}
    for book in result:
        names = re.split(r"\s*,?\s*and\s*|\s*,\s*", book['_authors'])
        for name in names:
            author_id = _authors.get(name)
            if author_id is None:
                ins = author.insert().values(name=name)
                result = conn.execute(ins)
                print(result.inserted_primary_key)
                author_id = result.inserted_primary_key[0]
                _authors[name] = author_id
            ins = authorship.insert().values(author_id=author_id, book_id=book.id)
            conn.execute(ins)

def downgrade():
    # Leave this for later.
    pass
