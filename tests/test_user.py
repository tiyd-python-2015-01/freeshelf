from freeshelf.models import User

def test_set_password():
    user = User(name="test", email="test@example.org")
    user.password = "testing"
    assert user.password == "testing"
    assert user.encrypted_password != "testing"
    assert user.check_password("testing")

def test_persistence(db):
    user = User(name="test", email="test@example.org", password="testing")
    db.session.add(user)
    db.session.commit()

    assert User.query.get(user.id) is user