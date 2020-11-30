import os
import sys

project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)

from django.conf.urls import url, include
from django.contrib import admin

app_name = "app01"
app_name = "appweb"
urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^app01/", include("app01.urls", namespace="app01")),
    url(r"^appweb/", include("appweb.urls", namespace="appweb")),
]
