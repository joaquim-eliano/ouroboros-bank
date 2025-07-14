import os

# URL do banco de dados SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ouroboros.db")

# Configurações de JWT
JWT_SECRET = os.getenv("JWT_SECRET", "troque_este_valor_por_um_segredo_forte")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")