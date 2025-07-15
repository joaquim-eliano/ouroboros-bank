import unittest
from PyQt5.QtWidgets import QApplication
from gui.login_dialog import LoginDialog
from services.auth_service import AuthService
from PyQt5.QtWidgets import QDialog

app = QApplication([])

class DummyAuth(AuthService):
    def __init__(self): pass
    def login(self, u, p):
        if u == 'user' and p == 'pass': return 'token123'
        raise Exception('Invalid')
    def register(self, u, p, e):
        if u and p and e: return True
        raise Exception('Bad Data')

class TestLoginDialog(unittest.TestCase):
    def setUp(self):
        self.auth = DummyAuth()
        self.dialog = LoginDialog(self.auth)

    def test_login_success(self):
        self.dialog.username_input.setText('user')
        self.dialog.password_input.setText('pass')
        self.dialog.login_button.click()
        self.assertEqual(self.dialog.jwt_token, 'token123')
        self.assertEqual(self.dialog.result(), QDialog.Accepted)

    def test_login_failure(self):
        self.dialog.username_input.setText('bad')
        self.dialog.password_input.setText('data')
        self.dialog.login_button.click()
        self.assertIsNone(self.dialog.jwt_token)
        self.assertEqual(self.dialog.result(), QDialog.Rejected)

    def test_register_success(self):
        self.dialog.switch_mode()
        self.dialog.username_input.setText('new')
        self.dialog.password_input.setText('pwd')
        self.dialog.email_input.setText('a@b.com')
        self.dialog.register_button.click()
        # após registro, volta ao modo login
        self.assertEqual(self.dialog.mode, 'login')

if __name__ == '__main__':
    unittest.main()