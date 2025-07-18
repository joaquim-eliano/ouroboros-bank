import hashlib
from datetime import datetime
from typing import List
from .transaction import Transaction

class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str = ''):
        self.index = index
        self.timestamp = datetime.utcnow().isoformat()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_header = f"{self.index}{self.timestamp}{self.previous_hash}{self.nonce}".encode()
        tx_hashes = b"".join(tx.compute_hash().encode() for tx in self.transactions)
        return hashlib.sha256(block_header + tx_hashes).hexdigest()

    def mine(self, difficulty: int) -> None:
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()
