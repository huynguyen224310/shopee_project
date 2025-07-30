import os
from dotenv import load_dotenv
import requests

load_dotenv()

PRODUCTION = os.getenv("PRODUCTION")
DEV = os.getenv("DEV")


def get_order_list(env_url):
    url = f'{env_url}/api/v2/order/get_order_list'

    headers = {}
    payload = {}
    with requests.Session() as session:
        try:
            resp = session.get(url, headers=headers, data=payload, allow_redirects=False)
            resp.raise_for_status()
            response = resp.json()
            order_list = [order.get('order_sn') for order in response["response"]["order_list"]]
            return env_url, session, order_list
        except requests.exceptions.RequestException as e:
            print(e)
            return None


def get_total_amount_order(env_url, session, order_list):
    list_order_completed = []
    url = f'{env_url}/api/v2/order/get_order_detail'
    payload = {'order_sn_list':''}
    headers = {}
    try:
        for i in range(0, len(order_list), 50):
            batch = order_list[i:i + 50]
            order_sn_str = ", ".join(batch)
            payload['order_sn_list'] = order_sn_str
            resp = session.get(url, headers=headers, data=payload, allow_redirects=False)
            resp.raise_for_status()
            response = resp.json()
            data = response["response"]["order_list"]
            for order in data:
                if order.get('order_status') == 'COMPLETED':
                    list_order_completed.append({'order_sn': order['order_sn'], 'order_status': order['order_status'],
                                         'total_amount': order['total_amount']})
        return list_order_completed

    except requests.exceptions.RequestException as e:
        print(e)
        return None

