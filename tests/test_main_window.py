import pytest
from PyQt5.QtCore import Qt        # <— adicione esta linha
from gui.main_window import MainWindow
from models.wallet import Wallet
from models.blockchain import Blockchain

def test_send_and_mine(qtbot):
    wallet = Wallet(user_id=1)
    blockchain = Blockchain(difficulty=1)
    window = MainWindow("dummy-token", blockchain, wallet)
    qtbot.addWidget(window)

    assert blockchain.pending_transactions == []

    qtbot.mouseClick(window.send_btn, Qt.LeftButton)   # agora Qt está definido
    assert len(blockchain.pending_transactions) == 1

    wallet.balance_ouro = 0.0
    qtbot.mouseClick(window.mine_btn, Qt.LeftButton)
    assert wallet.balance_ouro == 1.0
    assert blockchain.pending_transactions == []
