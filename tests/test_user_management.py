from freeshelf.models import User

def test_register(client):
    response = client.post('/register', data=dict(
        name="test",
        email="test@example.org",
        password="password",
        password_verification="password"
    ), follow_redirects=True)

    assert "registered and logged in" in str(response.data)


def test_login(client, session):
    user = User(name="test", email="test@example.org", password="password")
    session.add(user)
    session.commit()

    response = client.post('/login', data=dict(
        email="test@example.org",
        password="password"
    ), follow_redirects=True)

    assert "Logged in" in str(response.data)