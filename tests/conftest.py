import tempfile
import os

import pytest

from freeshelf import app as _app
from freeshelf import db as _db


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

_app.config.from_object(__name__)

@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope='function')
def db(app, request):
    """Session-wide test database."""
    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection)
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def client(app, db):
    return app.test_client()







