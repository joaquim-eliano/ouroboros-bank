# models/block_model.py
from sqlalchemy import Column, Integer, String
from .user import Base

class BlockModel(Base):
    __tablename__ = 'blocks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    index = Column(Integer, nullable=False, unique=True)
    timestamp = Column(String, nullable=False)
    previous_hash = Column(String, nullable=False)
    nonce = Column(Integer, nullable=False)
    hash = Column(String, nullable=False)
