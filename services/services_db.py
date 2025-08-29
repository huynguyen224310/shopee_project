from sqlalchemy.orm import Session
from database.db import engine
from database.models import OrderData
from sqlalchemy import func
from services.time_range import make_time_batches


def save_orders_orm(order_detail_list):
    if not order_detail_list:
        return 0

    inserted = 0
    with Session(engine) as session:
        for o in order_detail_list:
            pk = str(o["order_sn"])
            obj = session.get(OrderData, pk)
            if obj:
                obj.order_status = str(o["order_status"])
                obj.total_amount = float(o["total_amount"])
                obj.create_time = int(o["create_time"])
            else:
                session.add(OrderData(
                    order_sn=pk,
                    order_status=str(o["order_status"]),
                    total_amount=float(o["total_amount"]),
                    create_time=int(o["create_time"]),
                ))
            inserted += 1
        session.commit()
    return inserted


# Using database
def get_total_amount_by_time(
        order_status: str = None,
        ts_from: str = None,
        ts_to: str = None
) -> float:
    _, time_from, time_to = make_time_batches(ts_from, ts_to)
    with Session(engine) as session:
        q = session.query(func.sum(OrderData.total_amount))

        if time_from is not None:
            q = q.filter(OrderData.create_time >= time_from)
        if time_to is not None:
            q = q.filter(OrderData.create_time <= time_to)

        if order_status is not None:
            q = q.filter(OrderData.order_status == order_status)

        total = q.scalar()
        return float(total) if total is not None else 0.0
