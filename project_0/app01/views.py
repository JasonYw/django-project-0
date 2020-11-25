from django.shortcuts import render,HttpResponse
import random


# Create your views here.

def send_sms(request):
    '''
    发送短信
    '''
    code =random
    return HttpResponse('200')


def a(request):
    print('111')