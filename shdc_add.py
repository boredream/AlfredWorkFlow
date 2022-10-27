# coding:utf-8

import json
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


host = 'http://110.42.209.75/backend'
accountName = '18501683421@shinho.net.cn'
auth = '&accountName=%s' % accountName


def add_task():
    alfred_response = {"items": []}
    try:
        task_id = os.getenv("taskId")
        date = os.getenv('date')
        dish_list = os.getenv('dish_list').split(',')
    except IndexError:
        return

    for dish in dish_list:
        item = {"title": dish, "valid": "true"}
        subtitle = '点击提交新增 ' + date
        if task_id:
            subtitle = '点击提交修改' + date
        item['subtitle'] = subtitle
        item['variables'] = {"date": date, "dish": dish}

        alfred_response['items'].append(item)
    print(json.dumps(alfred_response))


add_task()
