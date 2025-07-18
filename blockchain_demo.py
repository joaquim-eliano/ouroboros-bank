from models.wallet import Wallet
from models.blockchain import Blockchain

if __name__ == '__main__':
    # Create wallets
    w1 = Wallet(user_id=1)
    w2 = Wallet(user_id=2)
    print("=== ADDRESSES ===")
    print(w1.get_address())
    print(w2.get_address())

    # Init blockchain
    bc = Blockchain(difficulty=2)
    print("Genesis hash:", bc.chain[0].hash)

    # Create and add tx
    tx = w1.create_signed_transaction(to_address=w2.get_address(), amount=10.0, fee=0.1)
    bc.add_transaction(tx)
    print("Pending tx:", [t.to_dict() for t in bc.pending_transactions])

    # Mine block
    bc.mine_pending_transactions(w1)
    print("Mined block #:", bc.chain[-1].index, "hash:", bc.chain[-1].hash)
    print("New balance for w1:", w1.balance_ouro)

    # Validate chain
    print("Valid?", bc.is_chain_valid())
