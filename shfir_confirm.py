# coding:utf-8

import json
import os
import sys

import requests


# 打包
def build_apk(env, project_root_path):
    build_cmd = 'cd ' + project_root_path + ' && '
    build_cmd += ('./gradlew assembleShinho' + ('Debug' if env == 'debug' else 'Release'))
    os.system(build_cmd)


# 获取上传凭证里的二进制apk信息
def get_api_token(env):
    bundle_id = 'com.archex.fsfa'
    if env == 'debug':
        bundle_id += '.debug'

    params = {
        "type": 'android',
        "bundle_id": bundle_id,
        'api_token': 'ec444bb63f54d06bdbd818149256dd5d'
    }
    url = 'http://api.bq04.com/apps'
    response = requests.post(url, params).content.decode('utf-8')
    binary = json.loads(response)['cert']['binary']
    return binary


# 上传文件
def upload_app_file(env, binary, project_root_path, file_name):
    env = 'debug' if env == 'debug' else 'release'
    app_name = 'SFA-DEBUG' if env == 'debug' else 'SFA'

    try:
        # 如果没有指定上传文件，则获取目录下最新apk文件信息
        apk_dir = project_root_path + 'app/build/outputs/apk/shinho/%s/' % env
        if not file_name:
            apk_info = json.load(open('%s/output.json' % apk_dir))[0]['apkInfo']
            file_name = apk_info['outputFile']

        version_name = file_name.split('_')[1]
        version_code = version_name.replace('.', '')
        if env == 'debug':
            version_code = version_code.replace('-debug', '')
        version_code = int(version_code)
        if version_code < 1000:
            version_code *= 10

        # 上传文件请求
        apk_file = {'file': open(apk_dir + file_name, 'rb')}
        param = {
            'key': binary['key'],  # 七牛上传 key
            'token': binary['token'],  # 七牛上传 token
            'x:name': app_name,
            'x:version': version_name,
            'x:build': version_code,
            'x:changelog': 'python upload ' + file_name,
        }
        req = requests.post(binary['upload_url'], files=apk_file, data=param)
        print(req.content)
    except Exception as e:
        print('上传失败' + str(e))


def main():
    # 为了查看进度，所以当前脚本使用 Terminal Command 打开。但要注意 Terminal Command 只能接收 query
    try:
        env = sys.argv[1]
        project_root_path = sys.argv[2]
        file_name = sys.argv[3]
    except IndexError:
        env = 'debug'
        project_root_path = '/Users/lcy/Documents/mobile-android/'
        file_name = None

    if not file_name:
        print('build new apk')
        build_apk(env, project_root_path)
        print('build done!')
        print('-------------------------')

    binary = get_api_token(env)
    print('get token done!')
    print('-------------------------')

    print('upload_app_file ...')
    upload_app_file(env, binary, project_root_path, file_name)
    print('all done!')


main()
