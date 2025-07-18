from typing import List
from .block import Block
from .transaction import Transaction

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
        if not transaction.signature:
            raise ValueError("Transaction must be signed")
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_wallet) -> Block:
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions.copy(),
            previous_hash=self.get_latest_block().hash
        )
        block.mine(self.difficulty)
        self.chain.append(block)

        reward_tx = miner_wallet.create_signed_transaction(
            to_address=miner_wallet.get_address(),
            amount=1.0
        )
        self.pending_transactions = [reward_tx]
        return block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
        return True
