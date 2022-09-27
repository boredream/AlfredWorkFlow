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
    try:
        date = os.getenv('date')
        dish = os.getenv('dish')
    except IndexError:
        sys.stdout.write("脚本参数错误")
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
    output = "%s %s\n点餐结果:%s" % (date, dish, content)
    sys.stdout.write(output)


add_task_commit()
