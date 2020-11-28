# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-11-25 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=32, verbose_name="用户名")),
                ("email", models.EmailField(max_length=32, verbose_name="邮箱")),
                ("phonenumber", models.CharField(max_length=32, verbose_name="手机号")),
                ("password", models.CharField(max_length=32, verbose_name="密码")),
            ],
        )
    ]
