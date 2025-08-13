import hmac
import json
import time
import requests
import hashlib

# Example
def shop_auth():
    timest = int(time.time())
    host = "https://partner.shopeemobile.com"
    path = "/api/v2/shop/auth_partner"
    redirect_url = "https://www.baidu.com/"
    partner_id = 80001
    tmp = "test...."
    partner_key = tmp.encode()
    tmp_base_string = "%s%s%s" % (partner_id, path, timest)
    base_string = tmp_base_string.encode()
    sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
    ##generate api
    url = host + path + "?partner_id=%s&timestamp=%s&sign=%s&redirect=%s" % (partner_id, timest, sign, redirect_url)
    print(url)

