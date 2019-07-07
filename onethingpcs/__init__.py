# coding=utf-8
# author:k2yk
# email:mzeyong@gmail.com

from . import config, common

import requests
import logging
import json


requests.packages.urllib3.disable_warnings()

class otc_api:
    request_handler = requests.session()
    download_handler = requests.session()
    user_info = {}
    turn_info = {}

    def __init__(self):
        self.request_handler.headers = {
            'User-Agent': "Mozilla/5.0",
            "cache-control": "no-cache"
        }
        self.request_handler.verify = False
        self.download_handler.headers = {
            'User-Agent': "Mozilla/5.0",
            "cache-control": "no-cache",
            "pathList":"/"
        }

    def login(self,user="",passwd=""): # 登陆
        try:
            login_data = common.body(deviceid=common.get_device_id(user), imeiid=common.get_imei_id(user), phone=user, pwd=common.get_pwd(passwd),
                                     account_type='4')
            result = self.request_handler.post(config.LOGIN_URL, data=login_data)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("iRet") == 0:
                    self.user_info["login"] = temp.get("data")
                    self.user_info["sessionid"] = self.request_handler.cookies.get("sessionid")
                    self.user_info["userid"] = self.request_handler.cookies.get("userid")
                    return True
        except Exception as error:
            logging.error("login:{0}".format(error))
        return False

    def get_login_info(self):  # 获取登陆信息
        return self.user_info.get("login")

    def account_info(self): # 账户信息
        try:
            account_data = common.get_params({"appversion": config.APP_VERSION}, self.user_info.get("sessionid"))
            result = self.request_handler.post(config.ACCOUNT_INFO_URL, data=account_data)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("iRet") == 0:
                    self.user_info["account_info"] = temp.get("data")
                    return temp
        except Exception as error:
            logging.error("account_info:{0}".format(error))
        return False

    def get_account_info(self):  # 获取账户信息
        return self.user_info.get("account_info")

    def list_peer_info(self): # 对端信息
        try:
            peer_data = common.get_params(dict(appversion=config.APP_VERSION, v="1", ct="1"), self.user_info.get("sessionid"), True)
            result = self.request_handler.get(config.LIST_PEER_URL + peer_data)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    self.user_info["all_peer_info"] = temp.get("result")[1]
                    return temp
        except Exception as error:
            logging.error("list_peer_info:{0}".format(error))
        return False

    def get_turn_server(self):
        try:
            peer_data = common.get_params(dict(appversion=config.APP_VERSION, ct="1",sn=self.user_info.get("all_peer_info").get("devices")[0].get("device_sn")),
                                          self.user_info.get("sessionid"), True)
            result = self.request_handler.get(config.GET_TURN_SERVER_URL + peer_data)
            if result.status_code == 200:
                temp = result.json()["turn_server_addr"]
                self.turn_info = temp
                return temp
        except Exception as error:
            logging.error("get_turn_server:{0}".format(error))
        return False

    def get_all_peer_info(self): # 获取对端信息
        return self.user_info.get("all_peer_info")

    def get_peer_id(self,nums = 0): # 获取任一对端ID
        try:
            result = self.user_info.get("all_peer_info")
            if result:
                temp = result["devices"]
                if len(temp)>nums and nums >=0:
                    return temp[nums].get("peerid")
        except Exception as error:
            logging.error("get_peer_id:{0}".format(error))
        return False

    def get_peer_device_id(self,nums = 0):  # 获取任一对端的设备ID
        try:
            result = self.user_info.get("all_peer_info")
            if result:
                temp = result["devices"]
                if len(temp)>nums and nums >=0:
                    return temp[nums].get("device_id")
        except Exception as error:
            logging.error("get_peer_id:{0}".format(error))
        return False

    def get_peer_info(self,nums=0):  # 获取任一对端设备信息
        try:
            result = self.user_info.get("all_peer_info")
            if result:
                temp = result["devices"]
                if len(temp)>nums and nums >=0:
                    return temp[nums]
        except Exception as error:
            logging.error("get_peer_info:{0}".format(error))
        return False

    def usb_info(self,deviceid=False): # 获取任一对端挂载硬盘信息
        try:
            if not deviceid:
                deviceid = self.get_peer_device_id()
            peer_data = common.get_params(dict(appversion=config.APP_VERSION, v="1", ct="1", deviceid=deviceid), self.user_info.get("sessionid"), True)
            result = self.request_handler.get(config.PEER_USB_INFO_URL + peer_data)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    self.user_info["usb_info"] = temp.get("result")
                    return temp
        except Exception as error:
            logging.error("account_info:{0}".format(error))
        return False

    def get_usb_info(self): # 返回对端挂在硬盘信息
        return self.user_info.get("usb_info")

    def load_session(self,sessionid,userid): # 读取对应的session /避免二次登陆
        try:
            requests.utils.add_dict_to_cookiejar(self.request_handler.cookies,{
                "sessionid":sessionid,
                "userid":userid
            })
            self.user_info["sessionid"]=sessionid
            self.user_info["userid"]=userid
            return True
        except Exception as error:
            logging.error("load_session:{0}".format(error))
        return False

    def get_session_info(self): # 返回对应的session
        return {
            "sessionid":self.user_info.get("sessionid"),
            "userid":self.user_info.get("userid")
        }

    def save_session(self,file_path="tmp_data.db"):  # 保存对应的session
        with open(file_path,"w") as temp_db:
            temp_db.write(json.dumps(self.get_session_info()))

    def list_remote_download(self,peerid=False):  # 获取对端远程下载列表
        try:
            if not peerid:
                peerid = self.get_peer_id()
            remote_dl_data = common.get_params(dict(pid=peerid, appversion=config.APP_VERSION, v="2", ct="31",
                                                    pos="0", needUrl="0",number="100",type="4"),
                                               self.user_info.get("sessionid"), True)
            result = self.request_handler.get(config.LIST_REMOTE_DOWNLOAD_LIST_URL + remote_dl_data)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    del temp["rtn"]
                    self.user_info["remote_download_list"] = temp
                    return temp
        except Exception as error:
            logging.error("list_remote_download:{0}".format(error))
        return False

    def get_list_remote_download_info(self): #  返回远端下载列表
        return self.user_info.get("remote_download_list")


    def remote_download_login(self,peerid=False): # 远端下载登陆
        try:
            if not peerid:
                peerid = self.get_peer_id()
            remote_dl_data = common.get_params(dict(pid=peerid, appversion=config.APP_VERSION, v="1", ct="32"),
                                               self.user_info.get("sessionid"), True)
            result = self.request_handler.get(config.LOGIN_REMOTE_DOWNLOAD_URL + remote_dl_data)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    del temp["rtn"]
                    self.user_info["remote_download_login"] = temp
                    return temp
        except Exception as error:
            logging.error("list_remote_download:{0}".format(error))
        return False

    def ansi_remote_download_url(self,url=False,peerid=False): # 解析远程下载的URL数据
        try:
            if not peerid:
                peerid = self.get_peer_id()
            post_data = {
                "url":url
            }
            result = self.request_handler.post(config.URLRESOLVE_REMOTE_DOWNLOAD_URL + "pid={0}&v=1".format(peerid), data=post_data)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    del temp["rtn"]
                    return temp
        except Exception as error:
            logging.error("list_remote_download:{0}".format(error))
        return False

    def create_remote_download_task(self,url,file_path=False,file_name=False,peerid=False):  # 创建远程下载任务
        try:
            if not peerid:
                peerid = self.get_peer_id()
            remoteinfo = self.ansi_remote_download_url(url=url)
            task_url , remote_dl_data = common.download_task(remoteinfo,file_path=file_path,file_name=file_name, userid=self.user_info.get("userid"))
            result = self.request_handler.post(task_url+"pid={}&v=2&ct=32".format(peerid),headers = {
                "Content-Type": "application/json"
            }, json=remote_dl_data)
            if result.status_code == 200:
                temp = result.json()
                if temp.get("rtn") == 0:
                    del temp["rtn"]
                    self.user_info["create_remote_download"] = temp
                    return temp
        except Exception as error:
            logging.error("list_remote_download:{0}".format(error))
        return False
