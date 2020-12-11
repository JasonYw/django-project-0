import os
import sys
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import random
import re

project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)
from appweb.models import UserInfo
from utils.tencent.sms import (
    LoginSMS,
    ReginterSMS,
    ResetPasswordSMS,
    RegisterUserSms,
    LoginUserSms,
    ResetPasswordSMS,
)
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
    phonenumber = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r"^(1[3-9]\d{9}$)", "手机号格式错误")],
        required=True,
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_phonenumber(self):
        # 手机号校验的钩子
        phonenumber = self.cleaned_data["phonenumber"]

        # 验证码类别的钩子
        functioncode = self.request.POST.get("functioncode")

        # 校验数据库中是否有模版
        if (
            functioncode != "register"
            and functioncode != "login"
            and functioncode != "restpassword"
        ):
            raise ValidationError("模板不存在")

        # 发短信&验证码
        code = random.randrange(1000, 9999)
        if functioncode == "register":
            if UserInfo.objects.filter(phonenumber=phonenumber).exists():
                # self.add_error('mobile_phone','短信模板错误') 与下一行效果等效
                raise ValidationError("手机号已存在")
            else:
                res = ReginterSMS.send_sms_single(phonenumber, code)
        if functioncode == "login":
            if not UserInfo.objects.filter(phonenumber=phonenumber).exists():
                raise ValidationError("手机号不存在")
            else:
                res = LoginSMS.send_sms_single(phonenumber, code)
        if functioncode == "restpassword":
            res = ResetPasswordSMS.send_sms_single(phonenumber, code)
        if res.get("result", None) != 0:
            raise ValidationError("短信发送失败")

        # 验证码写入redis
        conn = RegisterUserSms.record_register(phonenumber, code)
        return phonenumber


class ClickRegisterForm(forms.Form):

    email = forms.EmailField(
        label="邮箱",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入注册邮箱"}
        ),
        error_messages={"required": "邮箱不能为空"},
    )

    phonenumber = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r"^(1[3-9]\d{9}$)", "手机号格式错误")],
        required=True,
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

    username = forms.CharField(
        label="用户名",
        required=True,
        validators=[RegexValidator(r"^[0-9a-zA-Z\-_]{1,30}$", "用户名只支持数字字母以及-_")],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入用户名"}
        ),
        error_messages={"required": "用户名不能为空"},
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_email(self):

        email = self.request.POST.get("email")

        if UserInfo.objects.filter(email=email).exists():
            raise ValidationError("邮箱已经存在")

        return email

    def clean_password(self):
        password = self.request.POST.get("password")
        confirm_password = self.request.POST.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("密码两次不一致")

        return password

    def clean_phonenumber(self):
        code = self.request.POST.get("code")
        phonenumber = self.request.POST.get("phonenumber")
        if RegisterUserSms.get_record(phonenumber) != code:
            raise ValidationError("验证码错误")

        return phonenumber


class LoginPModelForm(forms.ModelForm):

    userid = forms.CharField(
        label="邮箱/手机号",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入注册邮箱/手机号"}
        ),
        error_messages={"required": "邮箱/手机号不能为空"},
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

    class Meta:
        model = UserInfo
        fields = ["userid", "password"]


class ClickLoginPForm(forms.Form):
    userid = forms.CharField(
        label="邮箱/手机号",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入注册邮箱/手机号"}
        ),
        error_messages={"required": "邮箱/手机号不能为空"},
    )

    password = forms.CharField(
        label="密码",
        required=True,
        validators=[RegexValidator(r"^[0-9a-zA-Z\-_@#\$%\&\=\+\!]+$", "密码格式错误")],
        max_length=20,
        min_length=8,
        error_messages={
            "required": "密码不能为空",
            "max_length": "密码不能超过20个字符",
            "min_length": "密码不能小于8个字符",
        },
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_userid(self):
        userid = self.request.POST.get("userid")
        print(userid)
        password = self.request.POST.get("password")
        email = re.findall(
            r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", userid
        )
        phonenumber = re.findall(r"^(1[3-9]\d{9}$)", userid)
        if email == phonenumber:
            raise ValidationError("格式错误")

        if len(phonenumber):

            if not UserInfo.objects.filter(phonenumber=userid).exists():
                raise ValidationError("手机号不存在")
            if UserInfo.objects.filter(phonenumber=userid).first().password != password:
                raise ValidationError("密码错误")
            else:
                self.request.session["email"] = email

        if len(email):

            if not UserInfo.objects.filter(email=userid).exists():
                raise ValidationError("邮箱不存在")
            if UserInfo.objects.filter(email=userid).first().password != password:
                raise ValidationError("密码错误")
            else:
                self.request.session["phonenumber"] = phonenumber

        return userid


class LoginSModelForm(forms.ModelForm):

    phonenumber = forms.CharField(
        label="手机号",
        required=True,
        validators=[RegexValidator(r"^(1[3-9]\d{9}$)", "手机号格式错误")],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入手机号"}
        ),
        error_messages={"required": "手机号不能为空"},
    )

    code = forms.CharField(
        label="验证码",
        required=True,
        validators=[RegexValidator(r"^\d{4}$", "验证码格式错误")],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入验证码"}
        ),
        error_messages={"required": "验证码不能为空"},
    )

    class Meta:
        model = UserInfo
        fields = ["phonenumber", "code"]


class ClickLoginSModelForm(forms.Form):

    phonenumber = forms.CharField(
        label="手机号",
        required=True,
        validators=[RegexValidator(r"^(1[3-9]\d{9}$)", "手机号格式错误")],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入手机号"}
        ),
        error_messages={"required": "手机号不能为空"},
    )

    code = forms.CharField(
        label="验证码",
        required=True,
        validators=[RegexValidator(r"^\d{4}$", "验证码格式错误")],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入验证码"}
        ),
        error_messages={"required": "验证码不能为空"},
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_phonenumber(self):
        phonenumber = self.request.POST.get("phonenumber")
        code = self.request.POST.get("code")
        if LoginUserSms.get_record(phonenumber) != code:
            raise ValidationError("验证码不正确")

        return phonenumber


# Create your models here.
