## E浙理自动健康申报
2021/11/4更新：已完成大幅度重构，提升了健壮度和稳定性。

## 使用方法
1. essentials.json记录了需要填报的账号和邮箱，修改之（如果不需要发邮件也可以不用写，不过得在main.py里注释相关代码）。  
2. email_config.json内指定了发件人smtp信息，修改之。
3. 请使用chrome浏览器，并下载相应版本的chromedriver，替换bin内chromedriver.exe

## 注意事项
1. 若需headless，需要自行修改构造函数nogui参数。
2. 默认关闭了chromedriver的logging。
3. 如果需要在Linux系统中运行，别忘了赋予chromedriver执行权限。
