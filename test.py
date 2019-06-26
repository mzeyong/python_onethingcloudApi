# coding=utf-8

import onethingpcs
otc = onethingpcs.otc_api()
login_status = otc.login(user="你的手机号",passwd="你的密码")
if login_status :
  print("登陆成功")
else:
  print("登陆失败")

### 获取远端信息
peer_status = otc.list_peer_info()
if peer_status:
  print("获取成功")
  print(otc.get_peer_info())
  print(otc.get_peer_id())
else:
  print("获取失败")

### 获取远端ID
print(otc.get_peer_id())



### 获取远端下载列表
dl_status = otc.list_remote_download()
if dl_status:
  print("获取成功")
  print(otc.get_list_remote_download_info())
else:
  print("获取失败")

### 创建下载任务

otc.create_remote_download_task("下载地址/magnet")

### 指定下载文件地址
otc.create_remote_download_task("下载地址/magnet",file_path="/media/sda1/onecloud/{}".format("your own path"))
