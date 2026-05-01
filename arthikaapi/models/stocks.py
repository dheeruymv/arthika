from database import Base
from sqlalchemy import Column, Integer, String, Float

class Stocks(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    quantity = Column(String(100))
    purchase_value = Column(Float)
    present_value = Column(Float)
    purchase_total = Column(Float)
    present_total = Column(Float)
    difference = Column(Float)
    user_id = Column(Integer)