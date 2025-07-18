from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QDialog, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from cryptography.hazmat.primitives import serialization

from gui.send_dialog import SendDialog
from gui.mine_dialog import MineDialog
from gui.blocks_view import BlocksView


class MainWindow(QMainWindow):
    def __init__(self, token: str, blockchain, wallet, user):
        super().__init__()
        self.setWindowTitle("Ouroboros Desktop")
        self.resize(600, 400)

        self.blockchain = blockchain
        self.wallet = wallet
        self.user = user

        # Layout principal
        central = QWidget()
        layout = QVBoxLayout(central)

        # Mostrar nick do usuário
        username_label = QLabel(f"Usuário: {self.user.username}")
        username_label.setFont(QFont("Arial", 12, QFont.Bold))
        username_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(username_label)

        # Mostrar chave pública resumida e botão copiar
        pubkey_pem = self.wallet.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        # Resumir a chave para exibir só parte dela (exemplo: primeira linha útil)
        lines = pubkey_pem.splitlines()
        if len(lines) > 2:
            short_key_display = lines[1][:20] + "..."
        else:
            short_key_display = pubkey_pem[:40] + "..."

        key_layout = QHBoxLayout()
        key_label = QLabel(f"Carteira: {short_key_display}")
        key_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # para poder selecionar texto manualmente

        copy_btn = QPushButton("Copiar")
        copy_btn.setToolTip("Copiar chave pública completa da carteira")

        def copiar_chave():
            clipboard = QApplication.clipboard()
            clipboard.setText(pubkey_pem)

        copy_btn.clicked.connect(copiar_chave)

        key_layout.addWidget(key_label)
        key_layout.addWidget(copy_btn)
        layout.addLayout(key_layout)

        # Saldo
        self.balance_label = QLabel(self._balance_text(), alignment=Qt.AlignCenter)
        layout.addWidget(self.balance_label)

        # Botões de ação
        self.send_btn = QPushButton("Enviar ORO")
        self.mine_btn = QPushButton("Minerar Bloco")
        self.view_blocks_btn = QPushButton("Histórico de Blocos")
        layout.addWidget(self.send_btn)
        layout.addWidget(self.mine_btn)
        layout.addWidget(self.view_blocks_btn)

        # Tabela de transações pendentes
        self.tx_table = QTableWidget(0, 3)
        self.tx_table.setHorizontalHeaderLabels(["De", "Para", "Valor"])
        layout.addWidget(self.tx_table)

        self.setCentralWidget(central)

        # Conectar sinais
        self.send_btn.clicked.connect(self._on_send)
        self.mine_btn.clicked.connect(self._on_mine)
        self.view_blocks_btn.clicked.connect(self._on_view_blocks)

        self._refresh_table()

    def _balance_text(self) -> str:
        return f"Saldo de Ouro: {self.wallet.balance_ouro:.4f}"

    def _refresh_table(self) -> None:
        pendings = self.blockchain.pending_transactions
        self.tx_table.setRowCount(len(pendings))
        for i, tx in enumerate(pendings):
            frm = tx.from_address if tx.from_address else "<mina>"
            self.tx_table.setItem(i, 0, QTableWidgetItem(str(frm)))
            self.tx_table.setItem(i, 1, QTableWidgetItem(str(tx.to_address)))
            self.tx_table.setItem(i, 2, QTableWidgetItem(f"{tx.amount:.4f}"))

    def _on_send(self) -> None:
        dlg: QDialog = SendDialog(self.wallet, self.blockchain, self)
        if dlg.exec() == QDialog.Accepted:
            self.balance_label.setText(self._balance_text())
            self._refresh_table()

    def _on_mine(self) -> None:
        dlg: QDialog = MineDialog(self.blockchain, self.wallet, self)
        if dlg.exec() == QDialog.Accepted:
            self.balance_label.setText(self._balance_text())
            self._refresh_table()

    def _on_view_blocks(self) -> None:
        dlg: QDialog = BlocksView(self.blockchain, self)
        dlg.exec()
