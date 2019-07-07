# coding=utf-8

import onethingpcs
# from onethingpcs.turnsession import test_turnsession
otc = onethingpcs.otc_api()
login_status = otc.login(user="您的手机号",passwd="您的密码")
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

### 获取turn信息
result = otc.get_turn_server()
print(result)


result = otc.get_usb_info()
print(result)
result = otc.get_list_remote_download_info()
print(result)
result = otc.list_remote_download()
print(result)
t = otc.create_remote_download_task("http://www.baidu.com",file_path="/tmp",file_name="passwd")
print(t)
print(result)

# import requests
# requests.get()
# conn,session = test_turnsession.main(**result)
# # session.send_channel_data()
# # import ssl
# # cotext = ssl.create_default_context()
# # scx = cotext.wrap_socket(conn)
# # conn.send()
# print(conn.recv(1024))
# print(temp)
#
# result = otc.get_turn_server()
# temp = stun.start_turn(**result)
# print(result)
# print(temp)


### 获取远端下载列表
# dl_status = otc.list_remote_download()
# if dl_status:
#   print("获取成功")
#   print(otc.get_list_remote_download_info())
# else:
#   print("获取失败")

### 创建下载任务

# otc.create_remote_download_task("下载地址/magnet")
#
# ### 指定下载文件地址
# otc.create_remote_download_task("下载地址/magnet",file_path="/media/sda1/onecloud/{}".format("your own path"))
