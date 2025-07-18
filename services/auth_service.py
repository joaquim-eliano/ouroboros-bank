# services/auth_service.py

import jwt
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from models.user import User
from persistence.sqlalchemy_repo import SQLAlchemyRepository
from config.settings import JWT_SECRET, JWT_ALGORITHM

class AuthService:
    def __init__(self, repo: SQLAlchemyRepository):
        self.repo = repo
        self.session = repo.session

    def register(self, username: str, password: str, email: str) -> User:
        """
        Cria um novo usuário.
        Parâmetros:
          - username
          - password
          - email
        Em caso de username/email duplicados, faz rollback e dispara ValueError.
        """
        try:
            # A ordem aqui bate com a chamada em LoginDialog.register_clicked:
            user = User.create(username=username, email=email, password=password)
            self.session.add(user)
            self.session.commit()
            return user
        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError("Username ou email já cadastrado") from exc
        except Exception:
            self.session.rollback()
            raise

    def login(self, username: str, password: str) -> str:
        """
        Valida credenciais e retorna um JWT.
        Faz rollback em caso de erro de sessão/DB.
        """
        try:
            user = (
                self.session
                    .query(User)
                    .filter_by(username=username)
                    .one_or_none()
            )
            if not user:
                raise ValueError("Usuário não encontrado")
            if not user.verify_password(password):
                raise ValueError("Senha inválida")

            payload = {
                "sub": str(user.id),
                "exp": datetime.utcnow() + timedelta(hours=1)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return token

        except ValueError:
            # falhas de credenciais não precisam rollback da sessão
            raise
        except Exception:
            self.session.rollback()
            raise

    def verify_token(self, token: str) -> dict:
        """
        Decodifica o JWT, disparando ValueError se for inválido ou expirado.
        """
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.PyJWTError as exc:
            raise ValueError("Token inválido") from exc
