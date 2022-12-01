# coding:utf-8

import json
import sys

project_root_path = sys.argv[1]

items = {"items": [
    {"title": "环境：Debug", "valid": "true", "variables": {
        "env": "debug",
        "fir_url": "http://hey.scandown.com/fsfadebug",
        "project_root_path": project_root_path
    }},
    {"title": "环境：Release", "valid": "true", "variables": {
        "env": "release",
        "fir_url": "http://hey.scandown.com/fsfapre",
        "project_root_path": project_root_path}
     },
]}
print(json.dumps(items))
