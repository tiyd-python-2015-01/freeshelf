import tempfile

import pytest

from freeshelf import create_app
from freeshelf.extensions import db as _db
from freeshelf.models import User, Book


dbfile = tempfile.NamedTemporaryFile(delete=False)
dbfile.close()

TEST_DATABASE_FILE = dbfile.name
TEST_DATABASE_URI = "sqlite:///" + TEST_DATABASE_FILE
TESTING = True
DEBUG = False
DEBUG_TB_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URI
WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(__name__)
    return app


@pytest.fixture
def db(app, request):
    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)

    _db.app = app
    return _db


@pytest.fixture
def user(db):
    user = User(name="test", email="test@example.org", password="password")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def book(db):
    book = Book(title="A Cool Book", url="http://example.org/book", authors="Some People")
    db.session.add(book)
    db.session.commit()
    return book



