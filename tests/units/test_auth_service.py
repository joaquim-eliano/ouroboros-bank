import pytest
from services.auth_service import AuthService
from persistence.sqlalchemy_repo import SQLAlchemyRepository
from models.user import User

class DummySession:
    def __init__(self):
        self.storage = []

    def add(self, obj):
        self.storage.append(obj)

    def commit(self):
        pass

    def query(self, model):
        class Q:
            def __init__(self, storage):
                self.storage = storage
            def get(self, _):
                return None
            def filter_by(self, **f):
                return [u for u in self.storage if all(getattr(u, k)==v for k,v in f.items())]

        return Q(self.storage)


@pytest.fixture
def repo():
    session = DummySession()
    return SQLAlchemyRepository(session)

@pytest.fixture
def auth(repo):
    return AuthService(repo)


def test_register_and_login(auth):
    user = auth.register("u", "u@e.com", "pass123")
    assert user.username == "u"
    token = auth.login("u", "pass123")
    assert isinstance(token, str)


def test_login_invalid(auth):
    with pytest.raises(ValueError):
        auth.login("naoexiste", "x")