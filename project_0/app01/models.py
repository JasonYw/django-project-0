from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
# Create your models here.
class UserInfo(models.Model):
    username =models.CharField(verbose_name='用户名',max_length=32)
    email =models.EmailField(verbose_name='邮箱',max_length=32)
    phonenumber =models.CharField(verbose_name='手机号',max_length=32)
    password =models.CharField(verbose_name='密码',max_length=32)


class RegisterModelForm(forms.ModelForm):
    
    phonenumber =forms.CharField(label='手机号',validators=[RegexValidator(r'^(1[3-9]\d{9}$)','手机号格式错误')])
    code =forms.CharField(label='短信验证码')
    password =forms.CharField(label="密码",widget=forms.PasswordInput())
    confirm_password =forms.CharField(label='重复密码',widget=forms.PasswordInput())

    class Meta:
        model =UserInfo
        fields ="__all__"
    

    def _init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = f'请输入{filed.label}'


