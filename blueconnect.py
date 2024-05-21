import json
import subprocess
import sys

is_connect = True
if len(sys.argv) > 1:
    is_connect = sys.argv[1] == '1'

# 替换为你的蓝牙设备名称
bluetooth_device_name = "RedmiBuds4Bore"

# 断开蓝牙设备
action = "--connect" if is_connect else "--disconnect"
args = ["/opt/homebrew/bin/blueutil", action, bluetooth_device_name]
result = subprocess.run(args, capture_output=True, text=True)

action_str = "蓝牙连接" if is_connect else "蓝牙断开"
detail_info = ''
if len(result.stderr) > 0:
    action_str += "失败"
    detail_info = result.stderr
else:
    action_str += "成功"

alfred_feedback = json.dumps({"items": [{"title": action_str, "subtitle": detail_info}]})
print(alfred_feedback)
