import jwt
from datetime import datetime, timedelta
from models.user import User
from persistence.sqlalchemy_repo import SQLAlchemyRepository
from config.settings import JWT_SECRET, JWT_ALGORITHM

class AuthService:
    def __init__(self, repo: SQLAlchemyRepository):
        self.repo = repo

    def register(self, username: str, email: str, password: str) -> User:
        user = User.create(username=username, email=email, password=password)
        return self.repo.save(user)

    def login(self, username: str, password: str) -> str:
        users = self.repo.get_by_filter(User, username=username)
        if not users:
            raise ValueError("Usuário não encontrado")
        user = users[0]
        if not user.verify_password(password):
            raise ValueError("Senha inválida")
        payload = {
            "sub": str(user.id),
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.PyJWTError as e:
            raise ValueError("Token inválido")