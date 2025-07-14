# Ouroboros Desktop

Aplicativo de banco digital fictício em Python com GUI PyQt5, banco SQLite, SQLAlchemy, Alembic para migrations, JWT e criptografia de senhas.

## Estrutura

- `models/` - Definição de entidades (User)
- `persistence/` - Repositório genérico SQLAlchemy
- `services/` - Lógica de negócio (AuthService)
- `config/` - Variáveis de ambiente e configurações
- `db/migrations/` - Scripts Alembic
- `tests/unit/` - Testes unitários
- `run.py` - Inicializa GUI e banco

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic init db/migrations  # se nunca tiver sido inicializado
alembic revision --autogenerate -m "create users table"
alembic upgrade head
pytest
# fim do README.md
