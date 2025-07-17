import sys
from PyQt5.QtWidgets import QApplication, QDialog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from config.settings import DATABASE_URL
# ORM declarative base and models
from models.user import Base, User as UserModel
from models.wallet import Wallet as WalletModel
# Generic repository for SQLAlchemy (assume takes only session)
from persistence.sqlalchemy_repo import SQLAlchemyRepository

# Business logic
from models.wallet import Wallet
from models.blockchain import Blockchain
from services.auth_service import AuthService
from gui.login_dialog import LoginDialog
from gui.main_window import MainWindow


def main():
    # --- 1) Database and ORM setup ---
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # --- 2) Repositories: instantiated with session only ---
    user_repo = SQLAlchemyRepository(session)
    wallet_repo = SQLAlchemyRepository(session)

    # --- 3) Auth service ---
    auth_service = AuthService(user_repo)

    # --- 4) Qt application and login dialog ---
    app = QApplication(sys.argv)
    login_dialog = LoginDialog(auth_service)
    if login_dialog.exec() != QDialog.Accepted:
        sys.exit(0)

    # Extract token and user_id
    token = login_dialog.jwt_token
    user_id = login_dialog.user_id

    # --- 5) Load or create wallet record ---
    wallet_record = wallet_repo.get_by_filter(user_id=user_id)
    if not wallet_record:
        logic_wallet = Wallet(user_id)
        pem = logic_wallet.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        wallet_record = WalletModel(
            user_id=user_id,
            public_key=pem.decode('utf-8'),
            balance_fiat=0.0,
            balance_ouro=0.0
        )
        wallet_repo.add(wallet_record)
        wallet_repo.commit()
    else:
        logic_wallet = Wallet(user_id)
        logic_wallet.balance_fiat = wallet_record.balance_fiat
        logic_wallet.balance_ouro = wallet_record.balance_ouro
        logic_wallet.public_key = serialization.load_pem_public_key(
            wallet_record.public_key.encode('utf-8'),
            backend=default_backend()
        )

    # --- 6) Initialize in-memory blockchain ---
    blockchain = Blockchain(difficulty=2)

    # --- 7) Show main window ---
    window = MainWindow(token, blockchain, logic_wallet)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
