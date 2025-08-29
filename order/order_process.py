import requests
from services.base_params import base_params
from services.time_range import make_time_batches
from services.services_db import save_orders_orm


def get_order_list(env_url, partner_id, partner_key, access_token, shop_id, time_from, time_to, order_status,
                   cursor=None):
    api_path = "/api/v2/order/get_order_list"
    url = f'{env_url}{api_path}'

    params = base_params(partner_id, partner_key, access_token, shop_id, api_path)
    params.update({
        "time_range_field": "create_time",
        "time_from": time_from,
        "time_to": time_to,
        "page_size": 100,
        "order_status": order_status
    })
    if cursor:
        params["cursor"] = cursor

    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json().get("response", {})


def get_all_orders(env_url, partner_id, partner_key, access_token, shop_id, time_from, time_to, order_status):
    order_sn_list = []
    list_time_batches = make_time_batches(time_from, time_to)
    for time_batch in list_time_batches:
        cursor = None
        while True:
            resp = get_order_list(env_url, partner_id, partner_key, access_token, shop_id, time_batch[0], time_batch[1],
                                  order_status, cursor=cursor)

            if not resp:
                break

            order_list = [order_sn.get("order_sn") for order_sn in resp.get("order_list", [])]
            order_sn_list.extend(order_list)
            if resp.get("more"):
                cursor = resp.get("next_cursor")
            else:
                break

    get_order_detail(env_url, partner_id, partner_key, access_token, shop_id, order_sn_list)


def get_order_detail(env_url, partner_id, partner_key, access_token, shop_id, order_sn_list):
    api_path = "/api/v2/order/get_order_detail"
    order_detail_list = []
    url = f'{env_url}{api_path}'
    for i in range(0, len(order_sn_list), 50):
        batch = order_sn_list[i:i + 50]
        params = base_params(partner_id, partner_key, access_token, shop_id, api_path)
        params["order_sn_list"] = ",".join(batch)

        # params["response_optional_fields"] = "order_sn,order_status,total_amount,create_time"

        resp = requests.get(url, params=params)
        resp.raise_for_status()
        order_list = resp.json().get("response", {}).get("order_list", [])
        # total_amount = 0
        for order in order_list:
            order_detail_list.append({
                "order_sn": order.get("order_sn"),
                "order_status": order.get("order_status"),
                "total_amount": order.get("total_amount"),
                "create_time": order.get("create_time")
            })
            # total_amount += order.get("total_amount")
    # print(total_amount)
    inserted = save_orders_orm(order_detail_list)
    if len(order_detail_list) == inserted:
        print("Số lượng bản ghi vào database khớp với response")
    print(f"Đã xử lý {inserted} đơn vào DB")

