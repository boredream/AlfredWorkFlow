# coding:utf-8

import json
import ssl
import os
import sys
import urllib.request
import urllib.parse

ssl._create_default_https_context = ssl._create_unverified_context


host = 'http://120.78.181.102:8080'
accountName = '18501683421@shinho.net.cn'
auth = '&accountName=%s' % accountName


def add_task_commit():
    alfred_response = {"items": []}
    try:
        date = os.getenv('date')
        dish = os.getenv('dish')
    except IndexError:
        alfred_response['items'].append({"title": "错误", "subtitle": "test"})
        print(json.dumps(alfred_response))
        return

    # 发送请求
    params = {
        "accountName": accountName,
        "orderDate": date,
        "orderDish": dish
    }
    url = host + '/api/meicanTask/addTask'
    request = urllib.request.Request(url, json.dumps(params).encode("utf-8"))
    request.headers = {
        "Content-Type": "application/json; charset=UTF-8",
    }
    content = urllib.request.urlopen(request).read()

    item = {"title": "日期:%s  点餐:%s" % (date, dish), "subtitle": "发送成功..." + content}
    alfred_response['items'][0] = item
    print(json.dumps(alfred_response))

sys.stdout.write("输出")