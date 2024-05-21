import hashlib
import random
import time
import uuid
import json
import ssl
import os
import sys
import urllib.request
import urllib.parse

# wechat https://developers.weixin.qq.com/doc/aispeech/confapi/dialog/token.html
app_id = '5VgPjdwxth2nfzX'
token = 'm793VZgsWMEQC4HMG9uOTr4yhoDNmG'
encodinng_aes_key = 'jRztKN8DQBPyD73xxfvoGfGSEnpL2ndwWTZoqQolbio'
host = 'https://openaiapi.weixin.qq.com'

# custom
user_id = 'eSIoMtkc5Qc'  # 操作数据的管理员 ID,可以点击官网右上角头像查看


# request
def send_request(path, body):
    nonce = 'bore.' + str(random.randint(1000000000, 9999999999))
    unix_timestamp = int(time.time())
    body = json.dumps(body)
    sign = gen_sign(token, unix_timestamp, body, nonce)

    header = {
        'Content-Type': 'application/json',
        # 'X-OPENAI-TOKEN': token,
        'X-APPID': app_id,
        'request_id': str(uuid.uuid4()),
        'timestamp': unix_timestamp,
        'nonce': nonce,
        'sign': sign
    }

    url = host + path

    print('request url ' + url)
    print('request header ' + json.dumps(header))
    print('request body ' + body)

    request = urllib.request.Request(url, method='POST', data=body.encode('utf-8'))
    request.headers = header
    content = urllib.request.urlopen(request, context=ssl._create_unverified_context()).read().decode('utf-8')
    print(content)


def gen_sign(request_token, unix_timestamp, body, nonce):
    body_md5 = hashlib.md5(body.encode('utf-8')).hexdigest()
    data = (request_token.encode('utf-8') +
            str(unix_timestamp).encode('utf-8') +
            nonce.encode('utf-8') +
            body_md5.encode('utf-8'))
    return hashlib.md5(data).hexdigest()


send_request('/v2/token', {
    "account": user_id
})



