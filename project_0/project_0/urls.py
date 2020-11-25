import os
import sys
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)

from django.conf.urls import url
from django.contrib import admin
from app01 import views
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^send/sms/',views.send_sms),
# ]

if __name__ =="__main__":
    views.a('1')