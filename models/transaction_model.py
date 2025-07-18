# models/transaction_model.py
from sqlalchemy import Column, Integer, Float, Text, String, ForeignKey
from .user import Base

class TransactionModel(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    from_address = Column(Text, nullable=False)
    to_address = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    nonce = Column(Integer, nullable=False)
    fee = Column(Float, default=0.0, nullable=False)
    data = Column(Text, nullable=True)
    timestamp = Column(String, nullable=False)
    signature = Column(Text, nullable=False)
    block_id = Column(Integer, ForeignKey('blocks.id'), nullable=True)
