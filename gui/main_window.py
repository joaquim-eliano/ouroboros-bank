# gui/main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem,
    QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, token: str, blockchain, wallet):
        super().__init__()
        self.setWindowTitle("Ouroboros Desktop")
        self.resize(600, 400)
        self.blockchain = blockchain
        self.wallet = wallet

        central = QWidget()
        layout = QVBoxLayout(central)

        # Saldo
        self.balance_label = QLabel(self._balance_text(), alignment=Qt.AlignCenter)
        layout.addWidget(self.balance_label)

        # Botões
        self.send_btn = QPushButton("Enviar ORO")
        self.mine_btn = QPushButton("Minerar Bloco")
        layout.addWidget(self.send_btn)
        layout.addWidget(self.mine_btn)

        # Tabela de transações pendentes
        self.tx_table = QTableWidget(0, 3)
        self.tx_table.setHorizontalHeaderLabels(["De", "Para", "Valor"])
        layout.addWidget(self.tx_table)

        self.setCentralWidget(central)

        # Conectar sinais
        self.send_btn.clicked.connect(self._on_send)
        self.mine_btn.clicked.connect(self._on_mine)

        self._refresh_table()

    def _balance_text(self) -> str:
        return f"Saldo de Ouro: {self.wallet.balance_ouro:.2f}"

    def _refresh_table(self) -> None:
        pendings = self.blockchain.pending_transactions
        self.tx_table.setRowCount(len(pendings))
        for i, tx in enumerate(pendings):
            frm = tx.from_address if tx.from_address else b"<mina>"
            self.tx_table.setItem(i, 0, QTableWidgetItem(str(frm)))
            self.tx_table.setItem(i, 1, QTableWidgetItem(str(tx.to_address)))
            self.tx_table.setItem(i, 2, QTableWidgetItem(str(tx.amount)))

    def _on_send(self) -> None:
        # Cria transação fixa para demonstrar funcionalidade
        from models.transaction import Transaction
        tx = Transaction(
            self.wallet.public_key,
            self.wallet.public_key,
            1.0,
            'ORO'
        )
        tx.sign(self.wallet.private_key)
        self.blockchain.add_transaction(tx)
        self._refresh_table()

    def _on_mine(self) -> None:
        block = self.blockchain.mine_pending_transactions(self.wallet)
        self.balance_label.setText(self._balance_text())
        self._refresh_table()
