import pytest

from freeshelf.models import User


@pytest.fixture
def user(session):
    user = User(name="test", email="test@example.org", password="password")
    session.add(user)
    session.commit()
    return user


def test_register(client):
    response = client.post('/register', data=dict(
        name="test",
        email="test@example.org",
        password="password",
        password_verification="password"
    ), follow_redirects=True)

    assert "registered and logged in" in str(response.data)


def login(user, client):
    return client.post('/login', data=dict(
        email=user.email,
        password=user.password
    ), follow_redirects=True)


def test_login(user, client):
    response = login(user, client)

    assert "Logged in" in str(response.data)


def test_logout(user, client):
    login(user, client)

    response = client.get('/logout',
                          follow_redirects=True)

    assert "Logged out" in str(response.data)