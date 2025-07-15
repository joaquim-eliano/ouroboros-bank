import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDialog
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL
from models.user import Base
from services.auth_service import AuthService
from gui.login_dialog import LoginDialog

class MainWindow(QMainWindow):
    def __init__(self, token: str):
        super().__init__()
        self.setWindowTitle("Ouroboros Desktop")
        self.setGeometry(100, 100, 600, 400)
        label = QLabel(f"Bem-vindo ao Ouroboros!\nToken: {token}", self)
        label.setAlignment(Qt.AlignCenter)

if __name__ == '__main__':
    # Configuração do banco
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Inicialização do app
    app = QApplication(sys.argv)
    auth_service = AuthService(session)
    login_dialog = LoginDialog(auth_service)

    # Execução do diálogo de login/registro
    if login_dialog.exec() == QDialog.Accepted:
        token = login_dialog.jwt_token
        window = MainWindow(token)
        window.show()
        sys.exit(app.exec_())
    else:
        # Sai se o usuário cancelar
        sys.exit()