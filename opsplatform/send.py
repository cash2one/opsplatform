# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: send.py
@time: 16-8-18 下午6:36
"""
from opsplatform import settings
import requests


def sms_send(mobiles, content):
    """ 调用短信借口发送信息
        GET 方式
        参数:
            mobile	必须	手机号码
            content	必须	发送内容
    """

    for mobile in mobiles:
        param = {'tos': mobile, 'content': content}
        r = requests.post(settings.SMS_INTERFACE, data=param)

