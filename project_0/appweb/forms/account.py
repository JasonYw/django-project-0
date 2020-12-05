import os
import sys
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from redis_cache import get_redis_connection

project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)
from appweb.models import UserInfo
import random
from utils.tencent.sms import LoginSMS, ReginterSMS, ResetPasswordSMS, RegisterUserSms
from django.shortcuts import HttpResponse


class RegisterModelForm(forms.ModelForm):

    email = forms.EmailField(
        label="邮箱",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入注册邮箱"}
        ),
        error_messages={"required": "邮箱不能为空"},
    )
    username = forms.CharField(
        label="用户名",
        required=True,
        validators=[RegexValidator(r"^[0-9a-zA-Z\-_]{1,30}$", "用户名只支持数字字母以及-_")],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入用户名"}
        ),
        error_messages={"required": "用户名不能为空"},
    )
    phonenumber = forms.CharField(
        label="手机号",
        required=True,
        validators=[RegexValidator(r"^(1[3-9]\d{9}$)", "手机号格式错误")],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入手机号"}
        ),
        error_messages={"required": "用户名不能为空"},
    )
    code = forms.CharField(
        label="短信验证码",
        required=True,
        validators=[RegexValidator(r"^\d{4}$", "验证码格式错误")],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请先获取短信验证码"}
        ),
        error_messages={"required": "短信验证码不能为空"},
    )
    password = forms.CharField(
        label="密码",
        required=True,
        validators=[RegexValidator(r"^[0-9a-zA-Z\-_@#\$%\&\=\+\!]+$", "密码格式错误")],
        max_length=20,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "请输入密码"}
        ),
        error_messages={
            "required": "密码不能为空",
            "max_length": "密码不能超过20个字符",
            "min_length": "密码不能小于8个字符",
        },
    )
    confirm_password = forms.CharField(
        label="重复密码",
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "请再次输入密码"}
        ),
        error_messages={"required": "重复密码与密码不匹配"},
    )

    class Meta:
        model = UserInfo
        fields = [
            "email",
            "phonenumber",
            "code",
            "username",
            "password",
            "confirm_password",
        ]


class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r"^(1[3-9]\d{9}$)", "手机号格式错误")],
        required=True,
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile_phone(self):
        # 手机号校验的钩子
        mobile_phone = self.cleaned_data["mobile_phone"]

        # 验证码类别的钩子
        functioncode = self.request.GET.get("functioncode")

        # 校验数据库中是否有手机号
        if UserInfo.objects.filter(phonenumber=mobile_phone).exists():
            raise ValidationError("手机号已存在")
        if (
            functioncode != "register"
            and functioncode != "login"
            and functioncode != "restpassword"
        ):
            raise ValidationError("模板不存在")

        # 发短信&验证码
        code = random.randrange(1000, 9999)
        if functioncode == "register":
            res = ReginterSMS.send_sms_single(mobile_phone, code)
        if functioncode == "login":
            res = LoginSMS.send_sms_single(mobile_phone, code)
        if functioncode == "restpassword":
            res = ResetPasswordSMS.send_sms_single(mobile_phone, code)
        if res.get("result", None) != 0:
            raise ValidationError("短信发送失败")

        # 验证码写入redis
        conn = get_redis_connection("default")
        conn = set(mobile_phone, code, ex=60)

        return mobile_phone


# Create your models here.
