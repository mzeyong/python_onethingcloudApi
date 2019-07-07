# 玩客云python api

### 使用教程

其中pwd的加密方式与sign值的获取方式学习参照了“不朽玩客云客户端”以及`tzwlwm`的相关代码，在此对代码作者表示感谢！！！
[不朽玩客云](https://github.com/Immortalt/imt-wanke-client)
[tzwlwm](https://github.com/tzwlwm/wky-python-client)

主要添加了远程下载文件的API ，自动下载对应的magent 以及普通文件。

摸鱼不易 点个star 再走吧


### 更新日期2019/7/7

新版本自定义了文件下载路径以及下载的文件名/文件夹名

更新了获取下载列表的参数，现在能正常获取下载列表了


准备开多两个branch 一个是部署在局域网的，一个是在广域网内通过turn打隧道的

下个更新看todolist

### 使用教程


使用方式如下：
```
import onethingpcs

### 登陆
otc = onethingpcs.otc_api()
login_status = otc.login(user="你的手机号",passwd="你的密码")
if login_status :
  print("登陆成功")
else:
  print("登陆失败")
  
### 获取远端信息
peer_status = otc.list_peer_info()
if peer_status :
  print("获取成功")
  print(otc.get_peer_info())
  print(otc.get_peer_id())
else:
  print("获取失败")


### 获取远端ID
print(otc.get_peer_id())
 
### 获取远端下载列表
dl_status = otc.list_remote_download()
if dl_status :
  print("获取成功")
  print(otc.get_list_remote_download_info())
else:
  print("获取失败")
  
### 创建下载任务

otc.create_remote_download_task("下载地址/magnet")

```

详情可查看test.py
