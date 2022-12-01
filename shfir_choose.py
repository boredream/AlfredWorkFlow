# coding:utf-8

import json
import os

env = os.getenv('env')
project_root_path = os.getenv('project_root_path')
if not env:
    env = 'debug'
if not project_root_path:
    project_root_path = '/Users/lcy/Documents/mobile-android/'

items = {"items": [
    {"title": "重新编译并上传", "valid": "true"},
]}

env = 'debug' if env == 'debug' else 'release'
app_name = 'SFA-DEBUG' if env == 'debug' else 'SFA'

# 获取目录下最新apk文件信息
apk_dir = project_root_path + 'app/build/outputs/apk/shinho/%s/' % env
if os.path.exists(apk_dir):
    files = os.listdir(apk_dir)
    files = sorted(files)
    # 倒序
    files.reverse()
    for file_name in files:
        if file_name.endswith('.apk'):
            items['items'].append({"title": file_name, "valid": "true", "variables": {"file_name": file_name}})

print(json.dumps(items))
