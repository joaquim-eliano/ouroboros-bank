from typing import Optional
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from .transaction import Transaction


class Wallet:
    def __init__(self, user_id: int):
        self.id = None
        self.user_id = user_id
        self.private_key = None
        self.public_key = None
        self.balance_fiat: float = 0.0
        self.balance_ouro: float = 0.0
        self.last_nonce = 0
        self.generate_keypair()

    def generate_keypair(self) -> None:
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def get_address(self) -> str:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")

    def create_signed_transaction(self, to_address: str, amount: float, fee: float = 0.0, data: Optional[str] = None) -> Transaction:
        self.last_nonce += 1
        tx = Transaction(
            from_address=self.get_address(),
            to_address=to_address,
            amount=amount,
            nonce=self.last_nonce,
            fee=fee,
            data=data
        )
        tx.sign(self.private_key)
        return tx

    @staticmethod
    def verify_signature(tx: Transaction) -> bool:
        from cryptography.hazmat.primitives.asymmetric import padding as _padding
        from cryptography.hazmat.primitives import hashes as _hashes
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        from cryptography.hazmat.backends import default_backend as _default_backend

        try:
            pubkey = load_pem_public_key(tx.from_address.encode(), backend=_default_backend())
            pubkey.verify(
                tx.signature,
                tx.serialize(),
                _padding.PSS(
                    mgf=_padding.MGF1(_hashes.SHA256()),
                    salt_length=_padding.PSS.MAX_LENGTH
                ),
                _hashes.SHA256()
            )
            return True
        except Exception:
            return False
