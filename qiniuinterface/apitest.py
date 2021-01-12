# -*- coding: utf-8 -*-
from qiniu.auth import *
import requests
import json
import sys


def apitest_post(apiurl,method,body,ak,sk):
    q = QiniuMacAuth(ak, sk)
    b=json.dumps(body)
    token = q.token_of_request(method="POST", host=None, url=apiurl, content_type="application/json",
                                   body=b, qheaders="")
    accessToken = 'Qiniu {0}'.format(token)
    curl_txt="curl -X POST " + str(apiurl) + " -H 'Authorization: " + str(
            accessToken) + "' -H 'Content-Type: application/json' -d '" + str(b) + "' -v"
    return curl_txt
def apitest_get(apiurl,method,ak,sk):
    q = QiniuMacAuth(ak, sk)
    token = q.token_of_request(method="GET", host=None, url=apiurl, content_type="application/json",
                            body=None, qheaders="")
    accessToken = 'Qiniu {0}'.format(token)
    curl_txt = "curl " + str(apiurl) + " -H 'Authorization: " + str(
            accessToken) + "' -H 'Content-Type: application/json' -v"
    return curl_txt