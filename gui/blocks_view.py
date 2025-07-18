from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
)
from PyQt5.QtCore import Qt

class BlocksView(QDialog):
    def __init__(self, blockchain, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Histórico de Blocos")
        self.resize(600, 400)
        self.blockchain = blockchain

        layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Índice", "Timestamp", "Hash", "#Tx"])
        layout.addWidget(self.table)
        self.close_btn = QPushButton("Fechar")
        layout.addWidget(self.close_btn)
        self.close_btn.clicked.connect(self.accept)

        self.populate()

    def populate(self):
        chain = self.blockchain.chain
        self.table.setRowCount(len(chain))
        for i, blk in enumerate(chain):
            self.table.setItem(i, 0, QTableWidgetItem(str(blk.index)))
            self.table.setItem(i, 1, QTableWidgetItem(blk.timestamp))
            self.table.setItem(i, 2, QTableWidgetItem(blk.hash[:16] + "..."))
            self.table.setItem(i, 3, QTableWidgetItem(str(len(blk.transactions))))