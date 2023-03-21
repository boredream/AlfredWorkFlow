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
    start_date = '2023-1-1'

if not end_date:
    today = datetime.datetime.today()
    end_date = today.strftime("%Y-%m-%d")


# start_date = '2023-2-24'
# end_date = '2023-3-13'

# 按条件筛选
# jql = 'project = SFA1 ' \
#       'AND resolution in (已解决, Done, 已完成, 完成) ' \
#       'AND 预计完成日期 >= %s AND 预计完成日期 <= %s' \
#       % (start_date, end_date)
jql = 'assignee in (21030087, 18020013, 21120065, 18070144, 18010089, 18070142, 20030015, 19040096) ' \
      'AND resolution in (已解决, Done, 已完成, 完成) ' \
      'AND 预计完成日期 >= %s AND 预计完成日期 <= %s' \
      % (start_date, end_date)
data = {
    "jql": jql,
    "decorator": "none",
    "maxResults": 300,
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
    story_point = int(task['fields']['customfield_10006'])
    user = task['fields']['assignee']['displayName']
    if user not in user_point:
        user_point[user] = story_point
    else:
        user_point[user] += story_point

total_point = 75
output = start_date + ' ~ ' + end_date + '\n'
for key, value in user_point.items():
    title = key + ' = ' + str(value)
    if value < 44:
        title += "【不足44】"
    output += title
    output += '\n'
    total_point += value

sys.stdout.write(output)
sys.stdout.write('总' + str(total_point))
sys.stdout.write('平均' + str(total_point / len(user_point.items())))

# alfred_response = {"items": []}
# for key, value in user_point.items():
#     title = key + '\t= ' + str(value)
#     if value < 44:
#         title += "【不足44】"
#     item = {"title": title}
#     alfred_response["items"].append(item)
#
# print(json.dumps(alfred_response))
