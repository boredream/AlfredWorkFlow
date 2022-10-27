# coding:utf-8

import datetime
import json
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context


host = 'http://110.42.209.75/backend'
accountName = '18501683421@shinho.net.cn'
accountPassword = 'Sh123456'
auth = '&accountName=%s' % accountName


def get_dish_list():
    url = host + '/api/meicanTask/dishList'

    request = urllib.request.Request(url)
    content = urllib.request.urlopen(request).read()
    dish_list = json.loads(content)['data']
    # 逗号拼接，作为整个字符串保存到变量
    return ','.join(dish_list).replace('/欣和专供', '').replace('/欣和企业专供', '')


def get_task_list():
    params = '?pageNo=1&pageSize=20&' + auth
    url = host + '/api/meicanTask/pageTask' + params

    request = urllib.request.Request(url)
    content = urllib.request.urlopen(request).read()
    return json.loads(content)['data']['records']


def show_task_list():
    # 获取所有菜单
    dish_list = get_dish_list()
    # 默认显示当前一周 + 下一周
    data_list = get_task_list()

    alfred_response = {"items": []}
    today = datetime.date.today()
    remainder_day = 14 - today.weekday()

    # 罗列从今天开始未来两周日期，默认未点餐
    for index in range(0, remainder_day):
        date = today + datetime.timedelta(index)

        # 跳过周末
        if date.weekday() >= 5:
            continue

        date_str = date.strftime("%Y-%m-%d")
        title = "[周%d] %s 【未点餐】" % (date.weekday() + 1, date_str)
        item = {"title": title, "subtitle": "点击添加", "valid": "true", "variables": {"date": date_str, "dish_list": dish_list}}
        alfred_response["items"].append(item)

    # 插入已点餐的日期
    for data in data_list:
        order_date = datetime.datetime.strptime(data["orderDate"], "%Y-%m-%d").date()
        day_diff = (order_date - today).days
        if day_diff < 0:
            # 昨天之前数据
            continue

        title = "[周%d] %s :%s" % (order_date.weekday() + 1, data["orderDate"], data["orderDish"])
        for index in range(0, len(alfred_response["items"])):
            if data["orderDate"] in alfred_response["items"][index]["title"]:
                alfred_response["items"][index] = {"title": title, "subtitle": "点击修改", "valid": "true",
                                                   "variables": {"taskId": data["uid"], "date": data["orderDate"], "dish_list": dish_list}}
                break

    print(json.dumps(alfred_response))


show_task_list()

