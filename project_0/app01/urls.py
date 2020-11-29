import os
import sys

project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)

from django.conf.urls import url, include
from django.contrib import admin
from app01 import views

urlpatterns = [url(r"^send/sms/", views.send_sms), url(r"^register/", views.register)]
