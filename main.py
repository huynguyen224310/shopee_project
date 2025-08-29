import os
from dotenv import load_dotenv
from database.db import create_database
from order.order_process import get_all_orders
from services.services_db import get_total_amount_by_time
load_dotenv()


def main():
    # create_database()
    # env_url = os.getenv("DEV")
    # partner_id = os.getenv("PARTNER_ID")
    # partner_key = os.getenv("PARTNER_KEY")
    # access_token = os.getenv("ACCESS_TOKEN")
    # shop_id = os.getenv("SHOP_ID")
    #
    # get_all_orders(env_url, partner_id, partner_key, access_token, shop_id, time_from, time_to, order_status)
    order_status = "COMPLETED"
    time_from = "1/12/2024"
    time_to = "1/1/2025"
    print(f'Tổng tiền bán đc từ {time_from} đến {time_to} : {get_total_amount_by_time(order_status, time_from, time_to)} VND')


if __name__ == "__main__":
    main()