# AndroidAutoMonkeyTest
使用Python进行monke自动化测试，并且将产生的error发送到指定的邮箱,
具体配置请将monkeyEmail.json对应的配置文件作出相应更改即可：

 - "time_format": "%Y%m%d_%H%M%S",  
 - "time_format_match": "%Y%m%d",
 - "file_type": "txt",
 - "pakeage": "com.android.brower",  #android的包名#
 - "delay": 200,  #monkey延迟#
 - "times": 1000,#monkey次数#
 - "param": "--ignore-crashes --ignore-timeouts --ignore-native-crashes --ignore-security-exceptions --pct-touch 80 --pct-motion 15 --pct-appswitch 5 --pct-rotation 0 -s 12358 -v -v -v --throttle", #monkey参数#
 -  "logs_path": "E://monkey//logs", #monkey log存储路径#
 -  "monkey_error_name": "monkey_error", #monkey错误文件名#
 -  "monkey_log_name": "monkey_log",#monkeylog文件名#
 - "from_addr": "xx@163.com", #发件人地址#
 -  "password": "xxxx", #base64加密的密码，不加密修改里面py即可#
 - "smtp_server":"smtp.exmail.qq.com", #smtp server#
 - "to_addr": ["xx@163.com","xx@163.com"],#收件人地址#
 - "to_user": "xx", #收件人名#
 - "to_addr": "xx@163.com", #收件人地址#
 -  "msg": "诗和远方" #邮件正文前缀，可调整py#
