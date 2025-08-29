from sqlalchemy import Column, String, Float, Integer
from database.db import Base


class OrderData(Base):
    __tablename__ = "order_data"

    order_sn = Column(String, primary_key=True, nullable=False)
    order_status = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    create_time = Column(Integer, nullable=False)
