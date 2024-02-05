#! /usr/bin/env python
# -*- coding:utf8 -*-

import sys
import json
import urllib.request
import urllib.parse

from configparser import ConfigParser

cp = ConfigParser()
cp.read('config.conf')
    
shid = cp.get('sh', 'shid')
pwd = cp.get('sh', 'pwd')

url = 'http://1.1.1.2/ac_portal/login.php'
data = {
    'opr': 'pwdLogin',
    'userName': shid,
    'pwd': pwd,
    'rememberPwd': 1,
}
data = urllib.parse.urlencode(data).encode("utf-8")
request = urllib.request.Request(url, data)
request.headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X -1_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
}
response = urllib.request.urlopen(request).read().decode('utf-8')
# response = "{'success':false, 'msg':'用户已在线，不需要再次认证','action':'location','pop':0,'userName':'18010089','location':''}"

response = response.replace('\'', '\"')
print(response)
msg = json.loads(response)['msg']

# item = {
#     "title": "标题",
#     "subtitle": "说明",
#     "valid": true,
#     "arg": "继续点击传递下一层query"
# }
items = {"items": [
    {"title": "登录结果", "subtitle": msg, "valid": "true", "arg": msg}
]}

print(json.dumps(items))
