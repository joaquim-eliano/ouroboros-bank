from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QCheckBox, QLabel
)
from services.auth_service import AuthService

class LoginDialog(QDialog):
    def __init__(self, auth_service: AuthService, parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.setWindowTitle("Login / Registro")
        self.mode = 'login'  # ou 'register'
        self.jwt_token = None
        self.user_id = None  # <-- Adicionado aqui

        # Layouts
        self.form_layout = QFormLayout()
        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        # Campos básicos
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.show_password_cb = QCheckBox("Mostrar senha")
        self.show_password_cb.stateChanged.connect(self.toggle_password_visibility)

        # Campo de e-mail (registro)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("somente para registro")
        self.email_input.hide()

        # Botões
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Registrar")
        self.switch_button = QPushButton("Ir para Registro")

        # Conectar sinais
        self.login_button.clicked.connect(self.login_clicked)
        self.register_button.clicked.connect(self.register_clicked)
        self.switch_button.clicked.connect(self.switch_mode)

        # Montar formulário
        self.form_layout.addRow("Usuário:", self.username_input)
        self.form_layout.addRow("Senha:", self.password_input)
        self.form_layout.addRow('', self.show_password_cb)
        self.form_layout.addRow("E-mail:", self.email_input)

        # Montar botões
        self.button_layout.addWidget(self.login_button)
        self.button_layout.addWidget(self.register_button)

        # Adicionar tudo ao layout principal
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.switch_button)
        self.setLayout(self.main_layout)

        self.update_ui()

    def toggle_password_visibility(self, state):
        if state == 2:  # Checked
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def switch_mode(self):
        self.mode = 'register' if self.mode == 'login' else 'login'
        self.update_ui()

    def update_ui(self):
        if self.mode == 'login':
            self.email_input.hide()
            self.login_button.show()
            self.register_button.hide()
            self.switch_button.setText("Ir para Registro")
        else:
            self.email_input.show()
            self.login_button.hide()
            self.register_button.show()
            self.switch_button.setText("Voltar ao Login")

    def login_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        try:
            token = self.auth_service.login(username, password)
            self.jwt_token = token

            # 🔐 Decodifica o token e extrai o ID do usuário
            payload = self.auth_service.verify_token(token)
            self.user_id = payload.get("sub")  # <- Define o user_id

            QMessageBox.information(self, "Sucesso", "Login realizado com sucesso.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Falha no login: {e}")

    def register_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        email = self.email_input.text().strip()
        try:
            self.auth_service.register(username, password, email)
            QMessageBox.information(self, "Sucesso", "Registro realizado com sucesso. Você já pode fazer login.")
            self.switch_mode()  # volta ao login
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Falha no registro: {e}")
