# -*- coding:utf-8 -*-
# Author: jacky
# Time: 14-2-22 下午11:48
# Desc: 短信http接口的python代码调用示例
import httplib

# 服务地址
import requests

host = "yunpian.com"
# 端口号
port = 80
# 版本号
version = "v1"
# 查账户信息的URI
user_get_uri = "/" + version + "/user/get.json"
# 通用短信接口的URI
sms_send_uri = "/" + version + "/sms/send.json"
# 模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_send.json"


def get_user_info(apikey):
    """
    取账户信息
    """
    conn = httplib.HTTPConnection(host, port=port)
    conn.request('GET', user_get_uri + "?apikey=" + apikey)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def send_sms(apikey, text, mobile):
    """
    能用接口发短信
    """
    payload = {'apikey': apikey, 'text': text, 'mobile': mobile}
    r = requests.post('http://%s:%s%s' % (host, port, sms_send_uri), data=payload)
    return r.text