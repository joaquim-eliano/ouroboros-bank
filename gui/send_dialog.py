from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDoubleSpinBox, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt


class SendDialog(QDialog):
    def __init__(self, wallet, blockchain, parent=None):
        super().__init__(parent)
        self.wallet = wallet
        self.blockchain = blockchain
        self.setWindowTitle("Enviar ORO")

        self.form = QFormLayout()
        self.recipient_input = QLineEdit()
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setDecimals(4)
        self.amount_input.setRange(0.0001, wallet.balance_ouro)
        self.fee_input = QDoubleSpinBox()
        self.fee_input.setDecimals(4)
        self.fee_input.setRange(0.0, wallet.balance_ouro)

        self.form.addRow("Destinatário:", self.recipient_input)
        self.form.addRow("Quantidade:", self.amount_input)
        self.form.addRow("Taxa (fee):", self.fee_input)

        self.send_btn = QPushButton("Assinar e Enviar")
        self.cancel_btn = QPushButton("Cancelar")

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.send_btn)
        btn_layout.addWidget(self.cancel_btn)

        main = QVBoxLayout(self)
        main.addLayout(self.form)
        main.addLayout(btn_layout)

        self.send_btn.clicked.connect(self.on_send)
        self.cancel_btn.clicked.connect(self.reject)

    def on_send(self):
        to_addr = self.recipient_input.text().strip()
        amount = self.amount_input.value()
        fee = self.fee_input.value()
        if not to_addr or amount <= 0:
            QMessageBox.warning(self, "Erro", "Preencha destinatário e valor válidos.")
            return
        if amount + fee > self.wallet.balance_ouro:
            QMessageBox.warning(self, "Erro", "Saldo insuficiente.")
            return
        try:
            tx = self.wallet.create_signed_transaction(
                to_address=to_addr,
                amount=amount,
                fee=fee
            )
            self.blockchain.add_transaction(tx)
            QMessageBox.information(self, "Sucesso", "Transação adicionada à mempool.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao enviar: {e}")
