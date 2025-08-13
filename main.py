import os
from dotenv import load_dotenv
from order.order import get_order_list, get_total_amount_order, create_params , create_time

load_dotenv()

BASE_URL = os.getenv('DEV')

def total_amount_order_in_time_range(start_time, end_time):
    order_status_list = ['SHIPPED','COMPLETED']
    time_list = create_time(start_time, end_time)
    params_list = create_params(time_list)
    total_amount_in_month = 0
    for order_status in order_status_list:
        order_sn_list = get_order_list(BASE_URL, params_list, order_status)
        total_amount_order = get_total_amount_order(BASE_URL, order_sn_list)
        total_amount_in_month += total_amount_order
    return total_amount_in_month

