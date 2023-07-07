#! /usr/bin/env python
# -*- coding:utf8 -*-

import json
import os
import re
import browser_cookie3
import requests


# 打包
def pack(project_root_path):
    # 读取配置里的 appId
    appid = ''
    file_path = project_root_path + '/src/manifest.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'"appid"\s*:\s*"([^"]+)"', content)
        if match:
            appid = match.group(1)
    if appid == '':
        print('appid not found in manifest.json')
        return

    # 使用命令行打包uni-app
    build_cmd = 'cd ' + project_root_path + ' && npm run build:app'
    os.system(build_cmd)
    print('cmd success: ' + build_cmd)

    # # 压缩成wgt文件
    # zip_wgt_cmd = 'cd ' + project_root_path + '/dist/build/app && zip -q -r ' + appid + '.wgt ./'
    # os.system(zip_wgt_cmd)
    # print('cmd success: ' + zip_wgt_cmd)
    # return project_root_path + '/dist/build/app/' + appid + '.wgt'

    # 直接获取压缩好的文件
    return project_root_path + '/dist/build/' + appid + '.wgt'


# 根据 appid 获取数字 id，后面上传用
def get_mp_num_id(token, mp_app_id):
    url = 'https://httpapi-test.shinho.net.cn/mpc-minipg/miniprogram/detail/' + mp_app_id
    headers = {
        'x-amz-security-token': token,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers)
    response_json = response.content.decode('utf-8')
    return str(json.loads(response_json)['data']['id'])


# 上传wgt
def upload_wgt(token, mp_id, wgt_path):
    # 获取版本号
    url = 'https://httpapi-test.shinho.net.cn/mpc-minipg/miniprogram/package/verion/get/' + mp_id
    headers = {
        'x-amz-security-token': token,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers)
    response_json = response.content.decode('utf-8')
    version = json.loads(response_json)['data']
    # print(version)

    # 获取上传文件
    file_path = wgt_path
    if not os.path.exists(file_path):
        print('file_path %s not exists' % file_path)
        return

    # 获取文件名称
    file_name = file_path.split('/')[-1]
    # print(file_name)

    # 获取上传凭证
    url = 'https://httpapi-test.shinho.net.cn/mpc-minipg/file/presignedUrl/package'
    data = {
        'fileName': file_name,
    }
    request = requests.post(url, data=json.dumps(data), headers=headers)
    response_json = request.content.decode('utf-8')
    response_data = json.loads(response_json)['data']
    upload_url = response_data['url']
    upload_file_path = response_data['filePath']

    # print(response_json)

    # 使用 multipart/form-data 上传文件
    headers = {
        'Content-Type': 'multipart/form-data'
    }
    files = {
        'file': open(file_path, 'rb')
    }
    requests.put(upload_url, headers=headers, files=files)
    # print('upload_app_file done!')

    # 提交小程序包信息
    file_size = os.path.getsize(file_path)
    data = {
        "mpId": mp_id,
        "mpVer": version,
        "commitId": "" + version,
        "unionId": file_name.split('.')[0],
        "packageUrl": upload_file_path,
        "desc": "upload by script",
        "fileName": file_name,
        "fileSize": file_size
    }
    headers = {
        'x-amz-security-token': token,
        'Content-Type': 'application/json'
    }
    url = 'https://httpapi-test.shinho.net.cn/mpc-minipg/miniprogram/package/upload'
    request = requests.post(url, data=json.dumps(data), headers=headers)
    response_json = request.content.decode('utf-8')
    response_body = json.loads(response_json)
    if response_body['code'] == 200:
        print('提交wgt包信息成功' + response_json)
        print('https://mpc-test.shinho.net.cn/mp/codePackage')
    else:
        print('提交wgt包信息失败' + response_json)


def commit_wgt(token, mp_app_id):
    # 先获取列表里第一个包
    package_list_url = 'https://httpapi-test.shinho.net.cn/mpc-minipg/miniprogram/package/list/' + mp_app_id
    headers = {
        'x-amz-security-token': token,
        'Content-Type': 'application/json'
    }
    data = {
        "page": 1,
        "pageSize": 10
    }
    package_list_request = requests.post(package_list_url, data=json.dumps(data), headers=headers)
    package_list_response = json.loads(package_list_request.content.decode('utf-8'))['data']
    # print('package_list_response = ' + package_list_response)

    # 判断第一个包是否是
    package_list = package_list_response['list']
    if len(package_list) <= 0:
        print('get mp package_list is empty')
        return
    package_id = package_list[0]['id']
    print('package_id = ' + str(package_id))

    # 然后将第一个包提测
    commit_test_url = 'https://httpapi-test.shinho.net.cn/mpc-minipg/miniprogram/package/submit/test/' + str(package_id)
    commit_audit_request = requests.post(commit_test_url, headers=headers)
    commit_audit_response = commit_audit_request.content.decode('utf-8')
    print('commit_audit_response = ' + commit_audit_response)

    # 提交审核
    commit_audit_url = 'https://httpapi-test.shinho.net.cn/mpc-minipg/miniprogram/package/test'
    data = {
        "packageId": package_id,
        "pass": True,
        "reason": "auto pass by script"
    }
    commit_audit_request = requests.post(commit_audit_url, data=json.dumps(data), headers=headers)
    commit_audit_response = commit_audit_request.content.decode('utf-8')
    print('commit_audit_response = ' + commit_audit_response)

    # # 发布上线
    commit_release_url = 'https://httpapi-test.shinho.net.cn/mpc-minipg/miniprogram/review/result'
    commit_release_request = requests.post(commit_release_url, data=json.dumps(data), headers=headers)
    commit_release_response = commit_release_request.content.decode('utf-8')
    print('commit_release_response = ' + commit_release_response)


def main():
    # TODO 修改成自己的数据
    mp_app_id = 'cfcb84a49d51486b8bfa64a2102141aa'  # 小程序app id
    project_root_path = '/Users/lcy/Documents/code/shinho/mpc-mp-template'  # 小程序项目地址

    user_token = ''
    for cookie in browser_cookie3.chrome(domain_name='shinho.net.cn'):
        if cookie.name.startswith('MPC_') and cookie.name.endswith('_TOKEN'):
            user_token = cookie.value
    if user_token == '':
        print('user_token not found')
        return
    print('get user token = ' + user_token)

    zip_wgt_path = pack(project_root_path)

    mp_id = get_mp_num_id(user_token, mp_app_id)  # 27
    print('get mp id = ' + mp_id)

    upload_wgt(user_token, mp_id, zip_wgt_path)
    commit_wgt(user_token, mp_app_id)


main()
