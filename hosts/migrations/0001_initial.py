# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-17 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostip', models.CharField(max_length=400, unique=True, verbose_name='ip地址')),
                ('port', models.CharField(max_length=200, verbose_name='主机端口')),
                ('username', models.CharField(max_length=100, verbose_name='主机用户名')),
                ('password', models.CharField(max_length=100, verbose_name='主机密码')),
                ('system_ver', models.CharField(default='', max_length=256, null=True, verbose_name='操作系统版本')),
                ('hostname', models.CharField(blank=True, max_length=200, null=True, verbose_name='主机名')),
                ('ssh_status', models.IntegerField(default=0, verbose_name='0-登录失败,1-登录成功')),
                ('mac_address', models.CharField(default='', max_length=512, verbose_name='mac地址列表')),
                ('sn', models.CharField(default='', max_length=256, verbose_name='SN－主机的唯一标示')),
            ],
            options={
                'verbose_name': '所有主机',
                'verbose_name_plural': '所有主机',
            },
        ),
    ]
