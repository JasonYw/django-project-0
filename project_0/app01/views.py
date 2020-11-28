import sys
import os
import json
import random
from django.shortcuts import render, HttpResponse
from app01 import models
from app01.models import RegisterModelForm, UserSms

project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)
from utils.tencent.sms import LoginSMS, ReginterSMS, ResetPasswordSMS

# Create your views here.


def send_sms(request):
    """
    发送短信
    """
    code = random.randrange(1000, 9999)
    phonenumber = request.POST.get("phonenumber")
    functioncode = request.POST.get("functioncode")

    if functioncode == "login":
        resobject = LoginSMS
    if functioncode == "register":
        resobject = ReginterSMS
    if functioncode == "resetpassword":
        resobject = ResetPasswordSMS
    # res =resobject.send_sms_single(phonenumber,code)
    res = {"result": 0}
    if res.get("result", None) == 0:
        UserSms.record_register(phonenumber, code, functioncode)
        return HttpResponse("200")
    else:
        return HttpResponse("请稍后重试")


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, "register.html", {"form": form})
    if request.method == "POST":
        obj = RegisterModelForm(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)
        else:
            print(obj.errors)
            return HttpResponse(json.dumps({"message": obj.errors}))
