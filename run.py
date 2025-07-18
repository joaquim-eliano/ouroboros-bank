import sys
import uuid
from PyQt5.QtWidgets import QApplication, QDialog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from config.settings import DATABASE_URL
from models.user import Base, User as UserModel
from models.wallet import Wallet as WalletLogic
from models.wallet_model import Wallet as WalletModel
from models.blockchain import Blockchain
from persistence.sqlalchemy_repo import SQLAlchemyRepository
from services.auth_service import AuthService
from gui.login_dialog import LoginDialog
from gui.main_window import MainWindow


def main():
    # --- Setup DB ---
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # --- Repos ---
    user_repo = SQLAlchemyRepository(session)
    wallet_repo = SQLAlchemyRepository(session)

    # --- Auth ---
    auth_service = AuthService(user_repo)

    # --- Login ---
    app = QApplication(sys.argv)
    login_dialog = LoginDialog(auth_service)
    if login_dialog.exec() != QDialog.Accepted:
        sys.exit(0)

    token = login_dialog.jwt_token
    user_id_str = login_dialog.user_id  # string uuid
    user_id = uuid.UUID(user_id_str)   # converte para UUID

    user = user_repo.get_by_id(UserModel, user_id)

    # --- Wallet ---
    wallet_record = wallet_repo.get_by_filter(WalletModel, user_id=user_id)
    if wallet_record is None:
        logic_wallet = WalletLogic(user_id)
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
        wallet_repo.save(wallet_record)
    else:
        logic_wallet = WalletLogic(user_id)
        logic_wallet.balance_fiat = wallet_record.balance_fiat
        logic_wallet.balance_ouro = wallet_record.balance_ouro
        logic_wallet.public_key = serialization.load_pem_public_key(
            wallet_record.public_key.encode('utf-8'),
            backend=default_backend()
        )

    # --- Blockchain ---
    blockchain = Blockchain(difficulty=2)

    # --- GUI ---
    window = MainWindow(token, blockchain, logic_wallet, user)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
