from django.shortcuts import HttpResponse, render, redirect
import sys
import os
import json
import random
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)
from utils.tencent.sms import LoginSMS, ReginterSMS, ResetPasswordSMS, RegisterUserSms
from appweb.forms.account import RegisterModelForm, SendSmsForm
from appweb.models import UserInfo


def send_sms(request):
    """
    发送短信
    """
    form = SendSmsForm(request, request.POST)  # 校验手机号不能为空、格式是否正确
    if form.is_valid():
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, "register.html", {"form": form})
    if request.method == "POST":
        obj = RegisterModelForm(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)
            message = {}
            if obj.cleaned_data.get("password") == obj.cleaned_data.get(
                "confirm_password"
            ) and obj.cleaned_data.get("code") == RegisterUserSms.get_record(
                obj.cleaned_data.get("phonenumber")
            ):
                del obj.cleaned_data["code"]
                del obj.cleaned_data["confirm_password"]
                UserInfo.objects.create(**obj.cleaned_data)
                return HttpResponse("200")
            if obj.cleaned_data.get("password") != obj.cleaned_data.get(
                "confirm_password"
            ):
                message["confirm_password"] = ["两次密码不相同"]
            if obj.cleaned_data.get("code") != RegisterUserSms.get_record(
                obj.cleaned_data.get("phonenumber")
            ):
                message["code"] = ["验证码不正确"]
            return HttpResponse(json.dumps({"status": "False", "message": message}))
