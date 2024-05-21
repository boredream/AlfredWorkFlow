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

# wechat work https://developer.work.weixin.qq.com/document/path/91039
corpid = 'ww18e17862584197f6'
# 考拉助手
corpsecret = 'DpT6c-uzLM5GZHCMWcTsUvPwUz45K-fOb5auBwafm5c'
host = 'https://qyapi.weixin.qq.com/cgi-bin'


# request
def get_access_token():
    url = host + '/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
    request = urllib.request.Request(url, method='GET')
    content = urllib.request.urlopen(request, context=ssl._create_unverified_context()).read().decode('utf-8')
    print(content)


my_access_token = '1fdqG3fYDl9b8aVC13yvxtsyaGAVWUNnn1U6aAqoIL5vcLn6y76pwEKrq0Ike2AYlxbx7Cp6tqi9Wi7Nq63L-ZiN_TOKH4NfyizihBGxlbGHklD3i25lBGm_WWCCnhiK5P_mlDNTeEi7P6_VkDdXpFdXRce57ciu_ixaCBnMjb4jm0__x_VK-0bYPVh8x6s93th2CnDXy3X6owJwoLoa-A'


def get_group_chat(chatid):
    url = host + '/appchat/get?access_token=' + my_access_token + '&chatid=' + chatid
    request = urllib.request.Request(url, method='GET')
    content = urllib.request.urlopen(request, context=ssl._create_unverified_context()).read().decode('utf-8')
    print(content)


get_group_chat('10870490335405243')
