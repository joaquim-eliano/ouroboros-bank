from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QProgressBar, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal

class MinerThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(object)
    def __init__(self, blockchain, wallet):
        super().__init__()
        self.blockchain = blockchain
        self.wallet = wallet

    def run(self):
        block = self.blockchain.mine_pending_transactions(self.wallet)
        self.finished.emit(block)

class MineDialog(QDialog):
    def __init__(self, blockchain, wallet, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Minerar Bloco")
        self.blockchain = blockchain
        self.wallet = wallet

        layout = QVBoxLayout(self)
        self.info = QLabel(f"Transações pendentes: {len(blockchain.pending_transactions)}")
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # indeterminate
        self.start_btn = QPushButton("Iniciar Mineração")

        layout.addWidget(self.info)
        layout.addWidget(self.progress)
        layout.addWidget(self.start_btn)

        self.start_btn.clicked.connect(self.start_mining)

    def start_mining(self):
        self.start_btn.setEnabled(False)
        self.thread = MinerThread(self.blockchain, self.wallet)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self, block):
        QMessageBox.information(self, "Minerado", f"Bloco #{block.index} minerado: {block.hash[:10]}...")
        self.accept()
