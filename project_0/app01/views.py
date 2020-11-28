import sys
import os
import json
import random
from django.shortcuts import render, HttpResponse
from .models import RegisterModelForm, UserInfo

project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)
from utils.tencent.sms import LoginSMS, ReginterSMS, ResetPasswordSMS, RegisterUserSms


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
    res = resobject.send_sms_single(phonenumber, code)
    # res = {"result": 0}
    if res.get("result", None) == 0:
        RegisterUserSms.record_register(phonenumber, code)
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

        else:
            print(obj.errors)
            return HttpResponse(json.dumps({"status": "False", "message": obj.errors}))


# if __name__ == "__main__":
#     print(UserSms.get_record('15801367721'))
