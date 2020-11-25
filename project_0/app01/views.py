import sys
import os 
import random
from django.shortcuts import render,HttpResponse
from app01 import models
from app01.models import RegisterModelForm
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)
from utils.tencent.sms import LoginSMS,ReginterSMS,ResetPasswordSMS

# Create your views here.

def send_sms(request):
    '''
    发送短信
    '''
    code =random.randrange(1000,9999)
    res =LoginSMS.send_sms_single('15801367721',code)
    if res.get('result',None) ==0:
        return HttpResponse('200')

    
def register(request):
    form =RegisterModelForm()
    return render(request,'register.html',{'form':form})