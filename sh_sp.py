# coding:utf-8

import datetime
import json
import sys

start_date = ''
end_date = ''
try:
    start_date = sys.argv[1]
    if '~' in start_date:
        end_date = start_date.split('~')[1]
        start_date = start_date.split('~')[0]
except IndexError:
    pass

# 结束日期到今天
today = datetime.datetime.today()
if end_date == '':
    end_date = today.strftime("%Y-%m-%d")
elif len(end_date) <= 5:
    end_date = str(today.year) + '-' + end_date

# 开始时间只传入 12-21 月日，自行补充年
start_date = str(today.year) + '-' + start_date

title = "点击回车查询「" + start_date + " - " + end_date + "」范围数据"
arg = "python3 sh_sp_confirm.py " + start_date + " " + end_date
print(json.dumps({"items": [{"title": title, "valid": "true",  "arg": arg, "variables":
    {"start_date": start_date, "end_date": end_date}}]}))
