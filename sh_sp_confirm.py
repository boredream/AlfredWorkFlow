# coding:utf-8
from urllib.parse import urlencode

# TODO Alfred 运行需要权限的命令（获取cookie）时，失败
import browser_cookie3

dict = browser_cookie3.chrome(domain_name='shinho.net.cn')

cookie = ''
for item in dict:
    cookie += (item.name + "=" + item.value + ";")

import ssl
import urllib.request
import os
import sys
import json
import datetime

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

ssl._create_default_https_context = ssl._create_unverified_context

start_date = ''
end_date = ''
if not start_date:
    try:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
    except IndexError:
        pass

if not start_date:
    start_date = '2023-7-1'

if not end_date:
    today = datetime.datetime.today()
    end_date = today.strftime("%Y-%m-%d")


def calculate(user_list):
    jql = 'assignee in (%s) AND resolution in (已解决, Done, 已完成, 完成) ' \
          'AND 预计完成日期 >= %s AND 预计完成日期 <= %s' \
          % (user_list, start_date, end_date)
    data = {
        "jql": jql,
        "decorator": "none",
        "maxResults": 999,
    }
    data = urlencode(data)

    url = 'http://jira.shinho.net.cn/rest/agile/1.0/epic/none/issue?' + data
    post_req = urllib.request.Request(url=url, headers={'Cookie': cookie})
    post_res_data = urllib.request.urlopen(post_req)
    content = post_res_data.read().decode('utf-8')
    response = json.loads(content)

    user_point = {}
    task_list = response['issues']
    for task in task_list:
        story_point = float(task['fields']['customfield_10006']) / 2
        user = task['fields']['assignee']['displayName']
        if user not in user_point:
            user_point[user] = story_point
        else:
            user_point[user] += story_point

    total_point = 0
    output = start_date + ' ~ ' + end_date + '\n'
    for key, value in user_point.items():
        title = key + ' = ' + str(value)
        if value < 22:
            title += "【不足22】"
        output += title
        output += '\n'
        total_point += value

    sys.stdout.write(output)


user_list_fore = \
    '17060036, ' \
    '18020013, ' \
    '18070144, ' \
    '18110018, ' \
    '20110074, ' \
    '21060033, ' \
    '21070016, ' \
    '21070106, ' \
    '21100053, ' \
    '21120065, ' \
    '22020020, ' \
    '22100018, ' \
    '21090069, ' \
    '17100021, ' \
    '18010089, ' \
    '18040185, ' \
    '21030087, ' \
    '21070032, ' \
    '21090068'

user_list_back = \
    '16010019, ' \
    '18120002, ' \
    '20030015, ' \
    '21050134, ' \
    '21100097, ' \
    '22030078, ' \
    '22040031, ' \
    '22040058, ' \
    '22110017, ' \
    '21030060, ' \
    '18070142, ' \
    '21020005, ' \
    '21050192, ' \
    '21060171, ' \
    '21070133, ' \
    '22030021, ' \
    '22080092'


user_list_test = '21030060'

# calculate(user_list_fore)

data = {"pageIndex": 1, "pageSize": 999, "issusType": ["子任务"], "sprintJiraId": 4024, "assignee": [], "parentJiraId": []}
data_json = json.dumps(data).encode(encoding='utf-8')

url = 'https://httpapi-prd.shinho.net.cn/dpl-api/group-manage/task-list'
post_req = urllib.request.Request(url=url, method='POST', data=data_json,  headers={'X-Amz-Security-Token': '824869d3a9b9e51306c354bfc4e904b5'})
post_res_data = urllib.request.urlopen(post_req)
content = post_res_data.read().decode('utf-8')
response = json.loads(content)
print(response)
