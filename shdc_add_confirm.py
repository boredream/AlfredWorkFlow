# coding:utf-8

import json
import ssl
import os
import sys
import urllib.request
import urllib.parse

ssl._create_default_https_context = ssl._create_unverified_context


host = 'http://124.70.194.85/backend'
accountName = '18501683421@shinho.net.cn'
auth = '&accountName=%s' % accountName


def add_task_commit():
    try:
        task_id = os.getenv('taskId')
        date = os.getenv('date')
        dish = os.getenv('dish')
    except IndexError:
        sys.stdout.write("脚本参数错误")
        return

    if task_id:
        # 发送请求 - 修改
        params = {
            "uid": task_id,
            "orderDish": dish
        }
        url = host + '/api/meicanTask/updateTask'
        request = urllib.request.Request(url, method='PUT', data=json.dumps(params).encode("utf-8"))
        request.headers = {
            "Content-Type": "application/json; charset=UTF-8",
        }
        content = urllib.request.urlopen(request).read()
        output = "%s %s\n点餐结果:%s" % (date, dish, content)
        sys.stdout.write(output)
    else:
        # 发送请求 - 新增
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
