## E浙理自动健康申报
2021/11/4更新：已完成大幅度重构，提升了健壮度和稳定性。

## 使用方法
1. essentials.json记录了需要填报的账号
2. email_config.json内指定了发件人smtp信息，修改之。如果不需要，请修改enabled字段为false
3. 请使用chrome浏览器，并下载相应版本的chromedriver，替换bin内chromedriver.exe

## 注意事项
1. 如需开启gui调试，请指定运行参数--gui
2. 默认关闭了chromedriver的logging，如需开启，请指定运行参数--chromedriver_logging
3. 如果需要在Linux系统中运行，别忘了赋予chromedriver执行权限。