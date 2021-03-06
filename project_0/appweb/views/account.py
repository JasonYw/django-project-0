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
from appweb.forms.account import (
    RegisterModelForm,
    SendSmsForm,
    ClickRegisterForm,
    LoginSModelForm,
    LoginPModelForm,
    ClickLoginPForm,
    ClickLoginSForm,
)
from appweb.models import UserInfo


def send_sms(request):
    """
    发送短信
    """
    obj = SendSmsForm(request, request.POST)  # 校验手机号不能为空、格式是否正确
    if obj.is_valid():
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "message": obj.errors})


def register(request):
    if request.method == "GET":
        obj = RegisterModelForm(request.GET)
        return render(request, "register.html", {"form": obj})
    if request.method == "POST":
        obj = ClickRegisterForm(request, data=request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)
            UserInfo.objects.create(**obj.cleaned_data)
            return JsonResponse({"status": True})
        else:
            print(obj.errors)
            return JsonResponse({"status": False, "message": obj.errors})


def login(request):
    if request.method == "GET":
        obj = LoginPModelForm(request.GET)
        if request.GET.get("way") == "sms":
            obj = LoginSModelForm(request.GET)
            return render(request, "logins.html", {"form": obj})
        return render(request, "login.html", {"form": obj})

    if request.method == "POST":
        if request.POST.get("way", None) == "sms":
            obj = ClickLoginSForm(request, data=request.POST)
        else:
            obj = ClickLoginPForm(request, data=request.POST)
        if obj.is_valid():
            return JsonResponse({"status": True, "message": 200})
        else:
            return JsonResponse({"status": False, "message": obj.errors})
