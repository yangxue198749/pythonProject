# -*- coding: utf-8 -*-
"""
@Time ： 2021/2/15 20:58
@Auth ： yangxue
@File ：sendRequest.py
@IDE ：PyCharm
@Motto：Done Never late

"""

# send_request.py

import requests
import json


class RunMethod:
    # post请求
    def do_post(self, url, data, headers=None):
        res = None
        if headers != None:
            res = requests.post(url=url, json=data, headers=headers)
        else:
            res = requests.post(url=url, json=data)
        return res.json()

    # get请求
    def do_get(self, url, data=None, headers=None):
        res = None
        if headers != None:
            res = requests.get(url=url, data=data, headers=headers)
        else:
            res = requests.get(url=url, data=data)
        return res.json()

    def run_method(self, method, url, data=None, headers=None):
        res = None
        print(method,url,data,headers)
        if method == "POST" or method == "post":
            res = self.do_post(url, data, headers)
        else:
            res = self.do_get(url, data, headers)
        return res


# if __name__=="__main__":
#     m=RunMethod()
#     res=m.run_method('post','url','data')
#     print(res)