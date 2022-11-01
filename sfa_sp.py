# coding:utf-8

import datetime
import json
import sys

start_date = ''
try:
    start_date = sys.argv[1]
except IndexError:
    pass

# 结束日期到今天
today = datetime.datetime.today()
end_date = today.strftime("%Y-%m-%d")

# 开始时间只传入 12-21 月日，自行补充年
start_date = str(today.year) + '-' + start_date

title = "点击回车查询「" + start_date + " - " + end_date + "」范围数据"
arg = "python3 sfa_sp_confirm.py " + start_date
print(json.dumps({"items": [{"title": title, "valid": "true",  "arg": arg, "variables":
    {"start_date": start_date, "end_date": end_date}}]}))
