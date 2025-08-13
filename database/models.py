from sqlalchemy import Column, String , Boolean
from .db import Base


class OrderData(Base):
    __tablename__ = 'order_data'
    order_sn = Column(String, primary_key=True)
    order_status = Column(String)
    total_amount = Column(Boolean)


