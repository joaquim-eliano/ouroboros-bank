import json
from datetime import datetime
from typing import Optional

class Transaction:
    def __init__(
        self,
        from_address: str,
        to_address: str,
        amount: float,
        nonce: int,
        fee: float = 0.0,
        data: Optional[str] = None
    ):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.nonce = nonce
        self.fee = fee
        self.data = data
        self.timestamp = datetime.utcnow().isoformat()
        self.signature: Optional[bytes] = None

    def serialize(self) -> bytes:
        obj = {
            "from": self.from_address,
            "to": self.to_address,
            "amount": self.amount,
            "nonce": self.nonce,
            "fee": self.fee,
            "data": self.data,
            "timestamp": self.timestamp
        }
        return json.dumps(obj, sort_keys=True).encode()

    def compute_hash(self) -> str:
        import hashlib
        return hashlib.sha256(self.serialize()).hexdigest()

    def sign(self, private_key) -> None:
        """Sign the serialized tx."""
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        data = self.serialize()
        self.signature = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def to_dict(self) -> dict:
        return {
            "from": self.from_address,
            "to": self.to_address,
            "amount": self.amount,
            "nonce": self.nonce,
            "fee": self.fee,
            "data": self.data,
            "timestamp": self.timestamp,
            "signature": self.signature.hex() if self.signature else None
        }