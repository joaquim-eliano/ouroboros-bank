import hashlib
from datetime import datetime
from typing import List
from .transaction import Transaction

class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str = ''):
        self.index = index
        self.timestamp = datetime.utcnow()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        tx_data = b"".join(tx.calculate_hash() for tx in self.transactions)
        block_string = f"{self.index}{self.timestamp}{tx_data}{self.previous_hash}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()