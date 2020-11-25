import sys
import os 
import random
from django.shortcuts import render,HttpResponse
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)
from utils.tencent import sms


# Create your views here.

def send_sms(request):
    '''
    发送短信
    '''
    code =random
    return HttpResponse('200')

if __name__ == "__main__":
    pass