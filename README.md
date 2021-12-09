## E浙理自动健康申报
2021/11/4更新：已完成大幅度重构，提升了健壮度和稳定性。
2021/12/9更新：已完成新的打卡系统的适配。

## 使用方法
1. essentials.json记录了需要填报的账号
2. email_config.json内指定了发件人smtp信息，修改之。如果不需要，请修改enabled字段为false
3. 请使用chrome浏览器，并下载相应版本的chromedriver，替换bin内chromedriver.exe

## 注意事项
1. 如需开启gui调试，请指定运行参数--gui
2. 默认关闭了chromedriver的logging，如需开启，请指定运行参数--chromedriver_logging
3. 如果需要在Linux系统中运行，别忘了赋予chromedriver执行权限。

## 简明教程
1. 修改essentials.json，确保账号密码邮箱正确。
2. 如果需要邮件提醒，请修改email_config.json，并确保enable字段为true，如果不需要则修改为false。
3. 安装最新版本的Chrome，下载与Chrome版本适配的Chromedriver（替换bin内的chromedriver.exe），请自行百度解决。
4. 安装Python3.6或更高的版本，确保安装requests库。
5. 运行程序。
