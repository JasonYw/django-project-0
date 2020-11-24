from django.shortcuts import render
from utils.tencent.sms import send_sms_single
import random
# Create your views here.

def send_sms(request):
    '''
    发送短信
    '''
    code =random
