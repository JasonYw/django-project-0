import os
import sys

project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)

from django.conf.urls import url, include
from django.contrib import admin
from appweb.views import account

urlpatterns = [
    url(r"^register/", account.register, name="register"),
    url(r"^send/sms/", account.send_sms, name="register"),
    url(r"^login/", account.login, name="register"),
]
