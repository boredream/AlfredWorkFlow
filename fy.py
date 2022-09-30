# coding:utf-8

import datetime
import json
import ssl
import sys
import urllib.request
import urllib.parse
import random
import hashlib


# 百度翻译 http://api.fanyi.baidu.com/doc/21
app_id = '20220930001362642'
app_secret = 'iK4eR2pM2OEgTctf4MO7'

try:
    query = sys.argv[1]
except IndexError:
    query = '你好'

# 签名生成方法
# 签名是为了保证调用安全，使用 MD5 算法生成的一段字符串，生成的签名长度为 32 位，签名中的英文字符均为小写格式。
#
# 生成方法：
# Step1. 将请求参数中的 APPID(appid)， 翻译 query(q，注意为UTF-8编码)，随机数(salt)，以及平台分配的密钥(可在管理控制台查看) 按照 appid+q+salt+密钥的顺序拼接得到字符串 1。
# Step2. 对字符串 1 做 MD5 ，得到 32 位小写的 sign。
# 注：
# 1. 待翻译文本（q）需为 UTF-8 编码；
# 2. 在生成签名拼接 appid+q+salt+密钥 字符串时，q 不需要做 URL encode，在生成签名之后，发送 HTTP 请求之前才需要对要发送的待翻译文本字段 q 做 URL encode；
# 3.如遇到报 54001 签名错误，请检查您的签名生成方法是否正确，在对 sign 进行拼接和加密时，q 不需要做 URL encode，很多开发者遇到签名报错均是由于拼接 sign 前就做了 URL encode；
# 4.在生成签名后，发送 HTTP 请求时，如果将 query 拼接在URL上，需要对 query 做 URL encode。


def trans(query):
    salt = random.randint(0, 100)
    sign = app_id + query + str(salt) + app_secret
    sign = hashlib.md5(sign.encode(encoding="UTF-8")).hexdigest()

    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    # url = 'http://fanyi-api.baidu.com/api/trans/vip/translate' \
    #       '?q=%s&from=zh&to=en&appid=%s&salt=%d&sign=%s' % (encode_query, app_id, salt, sign)
    data = {
        'q': query,
        'from': 'zh',
        'to': 'en',
        'appid': app_id,
        'salt': salt,
        'sign': sign,
    }

    data = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(url, data)
    request.headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    content = urllib.request.urlopen(request).read()
    return json.loads(content)['trans_result']


alfred_response = {"items": []}
result_list = trans(query)
for result in result_list:
    dst = result['dst']
    item = {"title": dst, "subtitle": "点击复制", "valid": "true", "arg": dst}
    alfred_response["items"].append(item)
print(json.dumps(alfred_response))
