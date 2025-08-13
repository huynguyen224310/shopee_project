import requests
import time
from datetime import datetime
from services.sign import shop_auth


def convert_date_string_to_timestamp(date_string):
    try:
        dt = datetime.strptime(date_string, "%d/%m/%Y")
        return int(dt.timestamp())
    except ValueError as e:
        print(e)
        return None


def create_time(time_start, time_end):
    max_seconds = 15 * 24 * 60 * 60
    time_from = convert_date_string_to_timestamp(time_start)
    time_to = convert_date_string_to_timestamp(time_end)
    time_range = time_to - time_from
    time_list = []
    while time_range > max_seconds:
        time_list.append((time_from, time_from + max_seconds))
        time_from += max_seconds
        time_range = time_to - time_from
    else:
        time_list.append((time_from, time_to))
    return time_list


def create_params(time_list):
    params_list = []
    for time_tuple in time_list:
        params = {
            "partner_id": "your_partner_id_here",
            "timestamp": "your_timestamp_here",
            "access_token": "your_access_token_here",
            "shop_id": "your_shop_id_here",
            "sign": shop_auth(),
            "time_range_field": "create_time",
            "time_from": time_tuple[0],
            "time_to": time_tuple[1],
            "page_size": 100,
            "cursor": ""
        }
        params_list.append(params)
    return params_list


def get_order_list(base_url, order_status, params_list):
    url = f'{base_url}/api/v2/order/get_order_list'
    headers = {}
    order_sn_list = []
    with requests.Session() as session:
        for params in params_list:
            params['order_status'] = order_status
            params['timestamp'] = int(time.time())
            while True:
                try:
                    resp = session.get(url, headers=headers, params=params, allow_redirects=False)
                    resp.raise_for_status()
                    response = resp.json()
                    order_sn_list.extend([order.get('order_sn') for order in response["response"]["order_list"]])
                    if response['response']['more'] is True:
                        params['cursor'] = response['response']['next_cursor']
                    else:
                        break
                except Exception as e:
                    print(e)
                    return None

    return order_sn_list


def get_total_amount_order(env_url, order_sn_list):
    list_order_completed = []
    url = f'{env_url}/api/v2/order/get_order_detail'
    headers = {}
    params = {
        "partner_id": "your_partner_id_here",
        "timestamp": "your_timestamp_here",
        "access_token": "your_access_token_here",
        "shop_id": "your_shop_id_here",
        "sign": shop_auth()}
    with requests.Session() as session:
        try:
            for i in range(0, len(order_sn_list), 50):
                batch = order_sn_list[i:i + 50]
                order_sn_str = ", ".join(batch)
                params['order_sn_list'] = order_sn_str
                resp = session.get(url, headers=headers, params=params, allow_redirects=False)
                resp.raise_for_status()
                response = resp.json()
                data = response["response"]["order_list"]
                for order in data:
                    list_order_completed.append(
                        {'order_sn': order['order_sn'], 'order_status': order['order_status'],
                         'total_amount': order['total_amount']})
            total_amount = calculate_total_amount(list_order_completed)
            return list_order_completed , total_amount

        except requests.exceptions.RequestException as e:
            print(e)
            return None

def calculate_total_amount(order_data):
    total = 0
    for order in order_data:
        total += order.get('total_amount', 0)
    return total