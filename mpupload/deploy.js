console.log('开始上传');

const path = require('path');
const fs = require('fs');
const axios = require('axios');
const headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

const configFilePath = path.resolve(__dirname, 'config.js');
if (!fs.existsSync(configFilePath)) {
    console.log('【发布失败】请参考「示例config.js」创建一份 config.js，并修改其中信息');
    return
}

const config = require('./config.js');

async function deploy() {
    const host = `https://httpapi-${config.env}.shinho.net.cn`;
    // get token
    try {
        let response = await axios.post(
            host + '/mpc-minipg/account/login',
            {
                "userName": config.shid,
                "password": config.pwd
            }, {headers})
        const user_token = response.data.data.token
        headers['X-Amz-Security-Token'] = user_token
        console.log('get user token = ', user_token);

        // get mp number id
        response = await axios.post(
            host + '/mpc-minipg/miniprogram/detail/' + config.mp_app_id,
            {}, {headers})
        const mp_number_id = response.data.data.id
        console.log('get mp number id = ', mp_number_id);

        // 获取版本号
        response = await axios.post(
            host + '/mpc-minipg/miniprogram/package/verion/get/' + mp_number_id,
            {}, {headers})
        const version = response.data.data
        console.log('get version = ', version);

        // 获取上传文件
        // 便利当前目录下的 .wgt 后缀文件
        const wgtList = fs.readdirSync(path.resolve(__dirname))
            .filter(item => item.endsWith('.wgt'))
        if(wgtList.length === 0) {
            console.log('脚本目录下缺少wgt文件')
            return
        }

        const fileName = wgtList[0]
        const unionId = fileName.replace('.wgt', '')
        // const filePath = path.resolve(__dirname, '..', 'dist/build/' + fileName)
        const filePath = path.resolve(__dirname, fileName)

        // 获取上传凭证
        response = await axios.post(
            host + '/mpc-minipg/file/presignedUrl/package',
            {"fileName": fileName}, {headers})
        const uploadFileUrl = response.data.data.url
        const uploadFilePath = response.data.data.filePath
        console.log('get upload token, path = ', uploadFilePath);

        // multipart/form-data 上传文件
        const FormData = require('form-data');
        const formData = new FormData();
        const file = fs.readFileSync(filePath);
        formData.append('file', file);
        response = await axios.put(uploadFileUrl, formData, {
            'Content-Type': 'multipart/form-data'
        })
        console.log('upload file success = ', response.status);

        // 提交小程序包信息
        const stats = fs.statSync(filePath);
        const fileSizeInBytes = stats.size;
        response = await axios.post(
            host + '/mpc-minipg/miniprogram/package/upload',
            {
                "mpId": mp_number_id,
                "mpVer": version,
                "commitId": "" + version,
                "unionId": unionId,
                "packageUrl": uploadFilePath,
                "desc": "upload by js script",
                "fileName": fileName,
                "fileSize": fileSizeInBytes
            }, {headers})
        console.log('upload package success = ', response.data);

        // 获取小程序包列表，并获取代提测的最新包
        response = await axios.post(
            host + '/mpc-minipg/miniprogram/package/list/' + config.mp_app_id,
            {
                "page": 1,
                "pageSize": 10
            }, {headers})
        const packageList = response.data.data.list
        if (packageList.length === 0) {
            console.log('ERROR: get package list EMPTY !');
            return
        }
        const package_id = packageList[0].id
        console.log('get ready upload package = ', package_id);

        // 将小程序包提交测试
        response = await axios.post(
            host + '/mpc-minipg/miniprogram/package/submit/test/' + package_id,
            {}, {headers})
        console.log('commit package success = ', response.data);

        // 提交审核
        response = await axios.post(
            host + '/mpc-minipg/miniprogram/package/test',
            {
                "packageId": package_id,
                "pass": true,
                "reason": "auto pass by js script"
            }, {headers})
        console.log('commit audit success = ', response.data);

        // 通过审核，发布上线
        response = await axios.post(
            host + '/mpc-minipg/miniprogram/review/result',
            {
                "packageId": package_id,
                "pass": true,
                "reason": "auto pass by js script"
            }, {headers})
        console.log('commit release success = ', response.data);

        // 获取App应用下所有小程序，匹配到目标小程序
        response = await axios.post(
            host + '/mpc-minipg/mp-manage/shopMallList',
            {
                'appId': config.app_id,
                'mpAppStatus': 1,
                'page': 1,
                'pageSize': 999
            }, {headers})
        const appMpList = response.data.data.list
        const appMp = appMpList.find(item => item.mpAppId === config.mp_app_id)

        if (!appMp) {
            // TODO 需要去商城首次添加
        } else {
            // 将应用的小程序版本更新到最新
            response = await axios.post(
                host + '/mpc-minipg/mp-manage/update',
                {
                    'appId': config.app_id,
                    'mpAppId': config.mp_app_id,
                    'mpCurrentVersion': appMp.mpVer,
                    'mpNewVersion': appMp.newVersion,
                    'packageId': appMp.id,
                }, {headers})
            console.log('update latest package success = ', response.data);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

deploy()
