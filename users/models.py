from django.db import models
from django.contrib.auth.models import AbstractUser


# 登录系统的用户信息
class Users(AbstractUser):
    STATUS_CHIOCE = (
        ('0', u'普通用户'),
        ('1', u'后台管理员'),
        ('2', u'超级管理员'),
    )
    # 0-普通用户, 1-后台管理员, 2-超级管理员
    user_level = models.CharField(default='0', max_length=2, choices=STATUS_CHIOCE,
                                  verbose_name=u'用户权限等级')

    class Meta:
        verbose_name = u'用户信息表'
        verbose_name_plural = verbose_name
        db_table = "userinfo"
