#!/usr/bin/env python
# -*- coding:utf-8 -*-
import ssl
import sys
import os
import redis
from qcloudsms_py import SmsMultiSender, SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

project_dir = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)
sys.path.append(project_dir)
from project_0 import settings

# ssl._create_default_https_context = ssl._create_unverified_context


APPKEY = settings.APPKEY
SMSSIGH = settings.SMSSIGN
SSDAPPID = settings.SSDAPPID
LOGINID = settings.LOGINID
REGISTERID = settings.REGISTERID
RESETPASSWORDID = settings.RESETPASSWORDID


class BaseSMS:
    APPID = ""
    EXPIRES = 10

    @classmethod
    def send_sms_single(cls, phone_num, randomcode):
        """
        单条发送短信
        :param  手机号
        :param  腾讯云短信模板ID
        :param  短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
        :return:
        """
        if cls.EXPIRES != None:
            param_list = [randomcode, cls.EXPIRES]
        else:
            param_list = [randomcode]
        sender = SmsSingleSender(SSDAPPID, APPKEY)
        try:
            response = sender.send_with_param(
                86, phone_num, cls.APPID, param_list, sign=SMSSIGH
            )
        except HTTPError as e:
            response = {"result": 1000, "errmsg": "网络异常发送失败"}
        return response


class LoginSMS(BaseSMS):
    APPID = LOGINID


class ReginterSMS(BaseSMS):
    APPID = REGISTERID


class ResetPasswordSMS(BaseSMS):
    APPID = RESETPASSWORDID
    EXPIRES = None


class BaseUserSms:
    conn = redis.Redis(
        host="192.168.1.18", port=6379, password="0125", encoding="utf-8"
    )

    @classmethod
    def record_register(cls, phonenumber, code, ex=600):
        cls.conn.set(phonenumber, str(code) + cls.functioncode, ex=ex)

    @classmethod
    def get_record(cls, phonenumber):
        if cls.conn.get(phonenumber) == None:
            return None
        return cls.conn.get(phonenumber).decode("utf-8").replace(cls.functioncode, "")


class RegisterUserSms(BaseUserSms):
    functioncode = "register"


class LoginUserSms(BaseUserSms):
    functioncode = "login"


class ResetpasswordUserSms(BaseUserSms):
    functioncode = "restpassword"


# def send_sms_multi(phone_num_list, template_id, param_list):
#     """
#     批量发送短信
#     :param phone_num_list:手机号列表
#     :param template_id:腾讯云短信模板ID
#     :param param_list:短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
#     :return:
#     """
#     appid = 112142311
#     sender = SmsMultiSender(appid, APPKEY)
#     try:
#         response = sender.send_with_param(86, phone_num_list, template_id, param_list, sign=SMSSIGH)
#     except HTTPError as e:
#         response = {'result': 1000, 'errmsg': "网络异常发送失败"}
#     return response

if __name__ == "__main__":
    print(APPKEY)
