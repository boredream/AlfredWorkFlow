# coding:utf-8

import json
import os
import sys

import requests


# 获取待上传文件和基本参数
def get_upload_file():
    project_root_path = sys.path[0]
    print(project_root_path)
    files = os.listdir(project_root_path)
    apk_file = None
    for file in files:
        if file.endswith(".apk") or file.endswith(".ipa"):
            apk_file = file
            break

    if not apk_file:
        return None

    return project_root_path + "/" + apk_file


# 上传文件
def upload_app_file(file_path):
    try:
        # 上传文件请求
        print("开始上传文件 " + file_path)
        apk_file = {'file': open(file_path, 'rb')}
        upload_url = 'http://c4idl.shinho.net.cn/api/app/version/upload'
        req = requests.post(upload_url, files=apk_file)

        return json.loads(req.content.decode('utf-8'))
        # {
        # 	"status": 0,
        # 	"data": {
        # 		"Location": "https://s3-045-shit-itplatform-uat-bjs.s3.cn-north-1.amazonaws.com.cn/app-manage/fsfa_4.9.1-debug_20221215_1554_debug.ac290c4251dd1.apk",
        # 		"Bucket": "s3-045-shit-itplatform-uat-bjs",
        # 		"Key": "app-manage/fsfa_4.9.1-debug_20221215_1554_debug.ac290c4251dd1.apk",
        # 		"ETag": "\"413cf83be8f528f70cbcd6a24e5a1f0b-11\""
        # 	},
        # 	"message": "success"
        # }
    except Exception as e:
        print('上传失败' + str(e))


# 保存版本信息
def save_version_info(user_key, file_name, env, s3id, s3url, version, file_size):
    try:
        params = {
            "title": file_name,
            "env": env,
            "s3id": s3id,
            "s3url": s3url,
            "version": version,
            "size": file_size,
            "groupId": 5,
            "updateIntro": "v" + version
        }
        # params = {
        #     "title": "fsfa_4.9.1-debug_20221215_1554_debug.apk",
        #     "env": "test",
        #     "s3id": "\"413cf83be8f528f70cbcd6a24e5a1f0b-11\"",
        #     "s3url": "https://s3-045-shit-itplatform-uat-bjs.s3.cn-north-1.amazonaws.com.cn/app-manage/fsfa_4.9.1-debug_20221215_1554_debug.2be7e02a18507.apk",
        #     "version": "4.9.1",
        #     "size": "52.68M",
        #     "groupId": 5,
        #     "updateIntro": "4.9.1"
        # }
        print("开始保存版本信息")
        url = 'http://c4idl.shinho.net.cn/api/app/version/create?userKey=' + user_key
        response = requests.post(url, params).content.decode('utf-8')
        print(response)
        print("[done]")
    except Exception as e:
        print('save_version_info error = ' + str(e))


def main():
    env = sys.argv[1]
    version = sys.argv[2]
    user_key = 'cfa5701177fe'

    upload_file_path = get_upload_file()
    if not upload_file_path:
        print("脚本所在目录下没有 .apk/.ipa 文件！")
        return

    upload_info = upload_app_file(upload_file_path)

    if upload_info['status'] != 0:
        print("上传文件失败 " + upload_info['message'])
    else:
        print("上传文件成功")
        file_name = upload_file_path.split('/')[-1]
        file_size = os.path.getsize(upload_file_path)
        file_size_name = format(file_size / 1000 / 1000, '.2f') + "M"
        s3id = upload_info['data']['ETag']
        s3url = upload_info['data']['Location']
        save_version_info(user_key, file_name, env, s3id, s3url, version, file_size_name)


main()
