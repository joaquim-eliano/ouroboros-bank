from typing import List
from .block import Block
from .transaction import Transaction
from .wallet import Wallet
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend

class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        genesis = Block(0, [], '0')
        self.chain.append(genesis)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction) -> None:
        if not transaction.from_address or not transaction.to_address:
            raise ValueError("Transaction must include from and to addresses")
        if not transaction.signature:
            raise ValueError("Transaction must be signed")
        pubkey = (
            load_pem_public_key(transaction.from_address, backend=default_backend())
            if isinstance(transaction.from_address, (bytes, bytearray))
            else transaction.from_address
        )
        if not Transaction.verify_signature(transaction.calculate_hash(), transaction.signature, pubkey):
            raise ValueError("Invalid signature")
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_wallet: Wallet) -> Block:
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions.copy(),
            previous_hash=self.get_latest_block().hash
        )
        block.mine_block(self.difficulty)
        self.chain.append(block)
        reward_tx = Transaction(
            None,
            miner_wallet.public_key,
            1.0,
            'ORO'
        )
        reward_tx.signature = b''
        miner_wallet.balance_ouro += 1.0
        self.pending_transactions = []
        return block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current, prev = self.chain[i], self.chain[i-1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
        return True
