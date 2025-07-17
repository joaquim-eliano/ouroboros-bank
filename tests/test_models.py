import pytest
from models.wallet import Wallet
from models.transaction import Transaction
from models.block import Block
from models.blockchain import Blockchain


def test_wallet_sign_verify():
    w = Wallet(user_id=1)
    data = b"hello"
    sig = w.sign_transaction(data)
    assert Wallet.verify_signature(data, sig, w.public_key)


def test_transaction_sign_verify():
    w = Wallet(user_id=2)
    tx = Transaction(
        w.public_key,
        w.public_key,
        10.0,
        'FIAT'
    )
    tx.sign(w.private_key)
    assert Transaction.verify_signature(tx.calculate_hash(), tx.signature, w.public_key)


def test_block_mining_and_hash():
    tx = Transaction(None, 'addr2', 5.0, 'ORO')
    block = Block(1, [tx], '0')
    block.mine_block(difficulty=1)
    assert block.hash.startswith('0')


def test_blockchain_operations():
    bc = Blockchain(difficulty=1)
    w = Wallet(user_id=3)
    tx = Transaction(
        w.public_key,
        w.public_key,
        2.0,
        'ORO'
    )
    tx.sign(w.private_key)
    bc.add_transaction(tx)
    block = bc.mine_pending_transactions(w)
    assert bc.is_chain_valid()
    assert w.balance_ouro == 1.0
