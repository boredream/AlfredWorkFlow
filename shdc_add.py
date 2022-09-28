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
        task_id = os.getenv("taskId")
        date = os.getenv('date')
        dish = sys.argv[1]
    except IndexError:
        alfred_response['items'].append({"title": "请输入菜品名称"})
        print(json.dumps(alfred_response))
        return

    subtitle = '点击提交新增'
    variables = {"date": date, "dish": dish}
    if task_id:
        subtitle = '点击提交修改'
        variables["taskId"] = task_id

    item = {"title": "日期:%s  点餐:%s" % (date, dish),
            "subtitle": subtitle,
            "valid": "true",
            "variables": {"date": date, "dish": dish}}
    alfred_response['items'].append(item)
    print(json.dumps(alfred_response))


add_task()
