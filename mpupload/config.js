// 因包含域账号敏感信息，所以需要额外处理，如下：
// 请复制当前文件在同目录下，并删除「示例」两字，用于编译脚本识别运行 结果 -> deploy/config.js
module.exports = {
  shid: '18010089', // 修改为您的工号
  pwd: 'Bore123123', // 修改为您的密码
  env: 'dev', // dev 或 test。生产环境不建议使用本脚本
  app_id: '68cfea7171524a3486158f9da90a6b69', // dev-sfa的应用id，可以替换成自己的
  mp_app_id: 'cc0399eb3d7748cc9b661b100ec3bcdb' // 当前小程序的 mpId
}
