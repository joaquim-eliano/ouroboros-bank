from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class Wallet:
    def __init__(self, user_id: int):
        self.id = None  # assigned by persistence layer
        self.user_id = user_id
        self.private_key = None
        self.public_key = None
        self.balance_fiat: float = 0.0
        self.balance_ouro: float = 0.0
        self.generate_keypair()

    def generate_keypair(self) -> None:
        """Generate a new RSA keypair."""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def sign_transaction(self, data: bytes) -> bytes:
        """Sign data with the wallet's private key."""
        if not self.private_key:
            raise ValueError("Private key not found")
        return self.private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    @staticmethod
    def verify_signature(data: bytes, signature: bytes, public_key) -> bool:
        """Verify a signature against data using a public key."""
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
