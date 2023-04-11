#! /usr/bin/env python
# -*- coding:utf8 -*-
import ssl
import sys
import json
import urllib.request
import urllib.parse

ssl._create_default_https_context = ssl._create_unverified_context

project_key = 'MPC'
# url = 'https://httpapi-prd.shinho.net.cn/dpl-api/group-manage/sprints-list?projectKey=' + project_key
url = 'https://httpapi-prd.shinho.net.cn/dpl-api/group-manage/task-list'

# {
#   "pageIndex": 1,
#   "pageSize": 999,
#   "issusType": [
#     "子任务"
#   ],
#   "sprintJiraId": 3697,
#   "assignee": [],
#   "parentJiraId": []
# }
data = {
    "pageIndex": 1,
    "pageSize": 999,
    "issusType": [
        "子任务"
    ],
    "sprintJiraId": 3697,
    "assignee": [],
    "parentJiraId": []
}
data = urllib.parse.urlencode(data).encode("utf-8")
request = urllib.request.Request(url)
request.headers = {
    "origin": "http://dpl.shinho.net.cn",
    "x-amz-security-token": "60df2eaad15e9b1919daed67a10b8fa7",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X -1_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
}
response = urllib.request.urlopen(request).read().decode('utf-8')
print(response)
