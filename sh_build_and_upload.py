# coding:utf-8

import json
import os
import sys
from configparser import ConfigParser

import requests


def get_user_key():
    print('start get_user_key')
    # cp = ConfigParser()
    # cp.read('config.conf')
    # shid = cp.get('sh', 'shid')
    # pwd = cp.get('sh', 'pwd')
    shid = '18010089'
    pwd = 'Bore123123'
    params = {
        "userName": shid,
        "password": pwd
    }
    url = 'http://c4idl.shinho.net.cn/api/login'
    req = requests.post(url, params)
    return json.loads(req.content.decode('utf-8'))


# 打包
def build_apk(env, project_root_path):
    build_cmd = 'cd ' + project_root_path + ' && '
    build_cmd += ('./gradlew assemble' + ('Debug' if env == 'debug' else 'Release'))
    build_cmd += (' -D org.gradle.java.home=/Applications/Android\ Studio.app/Contents/jre/Contents/Home')
    print('build cmd = ' + build_cmd)
    os.system(build_cmd)


# 上传文件
def upload_app_file(apk_info):
    try:
        # 上传文件请求
        print("开始上传文件 " + apk_info['apk_path'])
        apk_file = {'file': open(apk_info['apk_path'], 'rb')}
        upload_url = 'http://c4idl.shinho.net.cn/api/app/version/upload'
        req = requests.post(upload_url, files=apk_file)
        return json.loads(req.content.decode('utf-8'))
    except Exception as e:
        print('上传失败' + str(e))


# 保存版本信息
def save_version_info(user_key, project_id, file_name, env, s3id, s3url, version, file_size):
    try:
        params = {
            "title": file_name,  # fsfa_4.9.1-debug_20221215_1554_debug.apk
            "env": 'test',  # test
            "s3id": s3id,
            "s3url": s3url,
            "version": version,
            "size": file_size,  # 52.68M
            "groupId": project_id,
            "updateIntro": "upload by script"
        }
        print("开始保存版本信息")
        url = 'http://c4idl.shinho.net.cn/api/app/version/create?userKey=' + user_key
        response = requests.post(url, params).content.decode('utf-8')
        print(response)
        print("[done]")
    except Exception as e:
        print('save_version_info error = ' + str(e))


def get_apk_info(project_root_path, env):
    env = 'debug' if env == 'debug' else 'release'

    # 如果没有指定上传文件，则获取目录下最新apk文件信息
    package_dir = env
    # sfa 的在渠道下
    if 'mobile-android' in project_root_path:
        package_dir = 'shinho/' + env
    apk_dir = project_root_path + '/app/build/outputs/apk/%s/' % package_dir
    apk_info = json.load(open('%soutput-metadata.json' % apk_dir))['elements'][0]
    file_name = apk_info['outputFile']
    version_name = apk_info['versionName']
    version_code = apk_info['versionCode']

    return {
        'apk_path': apk_dir + file_name,
        'apk_file_name': file_name,
        'version_name': version_name,
        'version_code': version_code,
    }


def main():
    project_id = 5  # 4=c4i  5=sfa  15=mpc

    try:
        project_id = int(sys.argv[1])
    except IndexError:
        pass

    try:
        env = sys.argv[2]
    except IndexError:
        env = 'debug'

    project_root_path = ''
    if project_id == 4:
        project_root_path = '/Users/Bore/Documents/c4i/mobile/c4iapp/platforms/android'
    elif project_id == 5:
        project_root_path = '/Users/Bore/Documents/code/00shproject/mobile-android'
    elif project_id == 15:
        project_root_path = '/Users/Bore/Documents/code/shinho/mpc-android-template'

    if project_id == 0:
        print('project_id 不匹配')
        return

    print('project_id = %s , project_path = %s' % (project_id, project_root_path))

    # 打包
    print('build new apk %s' % env)
    build_apk(env, project_root_path)
    print('build done!')
    print('-------------------------')

    # 获取打包好的apk信息
    apk_info = get_apk_info(project_root_path, env)
    print('apk_info: %s' % apk_info)

    # 上传
    print('start upload file')
    upload_info = upload_app_file(apk_info)
    print('upload file response = ' + json.dumps(upload_info))

    if upload_info['status'] != 0:
        print('upload file error ' + upload_info['message'])
    else:
        print('upload file success')
        print('-------------------------')

        # get user key
        user_key = get_user_key()['data']
        print('get user key success = %s' % user_key)

        file_name = apk_info['apk_file_name']
        file_size = os.path.getsize(apk_info['apk_path'])
        file_size_name = format(file_size / 1000 / 1000, '.2f') + "M"
        s3id = upload_info['data']['ETag']
        s3url = upload_info['data']['Location']
        print('start update version info')
        save_version_info(user_key, project_id, file_name, env, s3id, s3url, apk_info['version_name'], file_size_name)
        print('update version info success')
    print('all done!')


main()
