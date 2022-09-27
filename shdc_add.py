# coding:utf-8

import json
import ssl
import sys
import os

ssl._create_default_https_context = ssl._create_unverified_context


host = 'http://120.78.181.102:8080'
accountName = '18501683421@shinho.net.cn'
auth = '&accountName=%s' % accountName


def add_task():
    alfred_response = {"items": []}
    try:
        date = os.getenv('date')
        dish = sys.argv[1]
    except IndexError:
        alfred_response['items'].append({"title": "请输入菜品名称"})
        print(json.dumps(alfred_response))
        return

    item = {"title": "日期:%s  点餐:%s" % (date, dish), "subtitle": "点击提交", "valid": "true", "variables": {"date": date, "dish": dish}}
    alfred_response['items'].append(item)
    print(json.dumps(alfred_response))


add_task()

