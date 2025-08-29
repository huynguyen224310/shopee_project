import time
import hmac
import hashlib


def base_params(partner_id, partner_key, access_token, shop_id, api_path):
    return {"partner_id": partner_id,
            "timestamp": int(time.time()),
            "access_token": access_token,
            "shop_id": shop_id,
            "sign": create_sign(partner_id, partner_key, access_token, shop_id, api_path),
            }


def create_sign(partner_id, partner_key, access_token, shop_id, api_path):
        return None

