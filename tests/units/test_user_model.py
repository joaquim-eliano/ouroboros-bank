import pytest
from models.user import User

@pytest.fixture
def password():
    return "senhaTeste123"

@pytest.fixture
def user(password):
    return User.create(username="joaquim", email="j@ex.com", password=password)


def test_password_hashing_different(password):
    u1 = User.create("u1", "u1@e.com", password)
    u2 = User.create("u2", "u2@e.com", password)
    assert u1.hashed_password != u2.hashed_password


def test_verify_password(user, password):
    assert user.verify_password(password)
    assert not user.verify_password("outraSenha")