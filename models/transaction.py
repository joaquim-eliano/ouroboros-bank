from datetime import datetime
from typing import Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Transaction:
    def __init__(
        self,
        from_address: Optional[any],
        to_address: any,
        amount: float,
        currency: str,
    ):
        self.id = None
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.currency = currency  # 'ORO' or 'FIAT'
        self.signature: Optional[bytes] = None
        self.timestamp = datetime.utcnow()
        self.status = 'PENDING'

    def calculate_hash(self) -> bytes:
        return f"{self.from_address}{self.to_address}{self.amount}{self.currency}{self.timestamp}".encode()

    def sign(self, private_key) -> None:
        """Sign this transaction."""
        self.signature = private_key.sign(
            self.calculate_hash(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    @staticmethod
    def verify_signature(data: bytes, signature: bytes, public_key) -> bool:
        try:
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False