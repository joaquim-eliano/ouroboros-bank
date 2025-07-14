import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    def verify_password(self, password: str) -> bool:
        salt, stored = self.hashed_password.split('$')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=base64.b64decode(salt),
            iterations=100_000,
            backend=default_backend()
        )
        try:
            kdf.verify(password.encode(), base64.b64decode(stored))
            return True
        except Exception:
            return False

    @classmethod
    def create(cls, username: str, email: str, password: str) -> 'User':
        salt = default_backend().osrandom_engine().urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )
        hashed = kdf.derive(password.encode())
        encoded = f"{base64.b64encode(salt).decode()}${base64.b64encode(hashed).decode()}"
        return cls(username=username, email=email, hashed_password=encoded)