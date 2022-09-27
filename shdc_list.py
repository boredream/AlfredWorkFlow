# coding:utf-8

import json
import ssl
import sys
import urllib.request
import datetime

ssl._create_default_https_context = ssl._create_unverified_context


host = 'http://120.78.181.102:8080'
accountName = '18501683421@shinho.net.cn'
accountPassword = 'Sh123456'
auth = '&accountName=%s' % accountName


def get_task_list():
    params = '?pageNo=1&pageSize=20&' + auth
    url = host + '/api/meicanTask/pageTask' + params

    request = urllib.request.Request(url)
    content = urllib.request.urlopen(request).read()
    return json.loads(content)['data']['records']


def show_task_list():
    # 默认显示当前一周 + 下一周
    data_list = get_task_list()

    alfred_response = {"items": []}
    today = datetime.date.today()
    first_date = today - datetime.timedelta(today.weekday())
    for index in range(0, 14):
        # 未点餐
        date = first_date + datetime.timedelta(index)
        # 跳过周末
        if date.weekday() >= 5:
            continue

        date_str = date.strftime("%m-%d")
        title = "[周%d] %s 【未点餐】" % (date.weekday() + 1, date_str)
        item = {"title": title, "subtitle": "点击添加", "valid": "true", "variables": {"date": date_str}}
        alfred_response['items'].append(item)

    for data in data_list:
        # 插入已点餐的日期
        order_date = datetime.datetime.strptime(data["orderDate"], "%Y-%m-%d").date()
        day_diff = (order_date - first_date).days

        date_str = order_date.strftime("%m-%d")
        title = "[周%d] %s  点餐:%s" % (order_date.weekday() + 1, date_str, data["orderDish"])
        alfred_response['items'][day_diff] = {"title": title, "subtitle": "已点餐", "valid": "true", "arg": ""}

    print(json.dumps(alfred_response))


show_task_list()

