# models/wallet_model.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from models.user import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    public_key = Column(String)
    balance_fiat = Column(Float)
    balance_ouro = Column(Float)
