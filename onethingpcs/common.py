# author:k2yk
# email:mzeyong@gmail.com

# Thanks to Immortalt Code
# https://github.com/Immortalt/imt-wanke-client

# Thanks to tzwlwm Code
# https://github.com/tzwlwm/wky-python-client

import hashlib
from . import config


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest().lower()


def get_imei_id(s):
    return md5(s)[0:16]

def get_device_id(s):
    return md5(s)[:14]


def get_pwd(passwd):
    s = md5(passwd)
    s = s[0:2] + s[8] + s[3:8] + s[2] +s[9:17] + s[27] + s[18:27] + s[17] + s[28:]
    return md5(s)

def get_sign(body, k=''):
    l = []
    while len(body) != 0:
        v = body.popitem()
        l.append(v[0] + '=' + v[1])
    l.sort()
    t = 0
    s = ''
    while t != len(l):
        s = s + l[t] + '&'
        t = t + 1
    s = s + 'key=' + k
    sign = md5(s)
    return sign


def body(**kwargs):
    result = {}
    for key in kwargs.keys():
        result[key] = kwargs[key]
    sign = get_sign(result)
    for key in kwargs.keys():
        result[key] = kwargs[key]
    result['sign']=sign
    return result

def get_params(data,sessionid,is_get=False):
    temp =[]
    result = {}
    for key in data.keys():
        if key == "pwd":
            temp.append(key+"="+get_pwd(data["pwd"]))
            result[key] = get_pwd(data[key])
        else:
            temp.append(key+"="+data[key])
            result[key] = data[key]
    sign = get_sign(result,sessionid)
    gstr = '&'.join(temp)
    if gstr:
        gstr += "&"
    key = "key="+sessionid
    estr=gstr+key+"&"

    return estr+"sign="+sign if not is_get else gstr +"sign="+sign

def download_task(file_info,userid="",file_name=False,file_path=False):
    result = {

    }
    if file_path and  not  file_path.startswith("/media/sda1/"):
        file_path = "/media/sda1/{}".format(file_path)
    if len(file_info.get("infohash")):
        result["btSub"]=[0]
        result["infohash"]=file_info.get("infohash")
        result["localfile"]=""
        result["name"]=file_info.get("taskInfo").get("name") if not file_name else file_name
        result["path"]="/media/sda1/onecloud/tddownload" if not file_path else file_path
        result["userid"]=userid
    else:
        result["path"]="/media/sda1/onecloud/tddownload" if not file_path else file_path
        result["tasks"]=[
            {
                "cid":"",
                "ext_json": {
                    "autoname": 1,
                    "userid": userid
                },
                "filesize":0,
                "gcid":"",
                "name":file_info.get("taskInfo").get("name") if not file_name else file_name,
                "ref_url":"",
                "url":file_info.get("taskInfo").get("url")

            }
        ]
    return config.CREATE_REMOTE_BT_DOWNLOAD_TASK_URL if len(file_info.get("infohash")) else config.CREATE_REMOTE_DOWNLOAD_TASK_URL, result



