
# -*- coding: utf-8 -*-
from qiniu.auth import *
import requests
import json
import sys

def cli_post(apiurl,method,body,ak,sk):
    q = QiniuMacAuth(ak, sk)
    b=json.dumps(body)
    print(body)
    print(b)
    token = q.token_of_request(method="POST", host=None, url=apiurl, content_type="application/json",
                                   body=b, qheaders="")
    accessToken = 'Qiniu {0}'.format(token)
    headers = {}
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = accessToken
    res = requests.post(apiurl,data=b,headers=headers)
    return res
def cli_get(apiurl,method,ak,sk):
    q = QiniuMacAuth(ak, sk)
    token = q.token_of_request(method="GET", host=None, url=apiurl, content_type="application/json",
                            body=None, qheaders="")
    accessToken = 'Qiniu {0}'.format(token)
    headers = {}
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = accessToken
    print("1111")
    res = requests.get(apiurl,headers=headers)
    print(res)
    return res