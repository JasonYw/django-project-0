from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
import redis

# Create your models here.


class UserSms:
    conn = redis.Redis(
        host="192.168.1.18", port=6379, password="0125", encoding="utf-8"
    )

    @classmethod
    def record_register(cls, phonenumber, code, functioncode):
        cls.conn.set(phonenumber, str(code) + functioncode, ex=600)

    @classmethod
    def get_record(cls, phonenumber):
        cls.conn.get(phonenumber)


class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    email = models.EmailField(verbose_name="邮箱", max_length=32)
    phonenumber = models.CharField(verbose_name="手机号", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)


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

    # def _init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     for name,field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['placeholder'] = f'请输入{filed.label}'
