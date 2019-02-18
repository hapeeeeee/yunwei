from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Host(models.Model):
    hostowner = models.ForeignKey(User, verbose_name='主机所有者')
    hostip = models.CharField(max_length=400,verbose_name='ip地址', unique=True)
    port = models.CharField(max_length=200,verbose_name='主机端口')
    username = models.CharField(max_length=100, verbose_name='主机用户名')
    password = models.CharField(max_length=100, verbose_name='主机密码')
    system_ver = models.CharField(max_length=256, null=True, verbose_name=u"操作系统版本", default="")
    hostname = models.CharField(max_length=200, verbose_name='主机名', blank=True, null=True)
    host_name = models.CharField(max_length=256, null=True, verbose_name=u"操作系统主机名", default="")
    ssh_status = models.IntegerField(verbose_name=u"0-登录失败,1-登录成功", default=0)
    mac_address = models.CharField(max_length=512, verbose_name=u"mac地址列表", default="")
    sn = models.CharField(max_length=256, default='', verbose_name=u"SN－主机的唯一标示")
    def __str__(self):
        return '{}的{}'.format(self.hostowner, self.hostname)

    def keys(self):

        return ('hostip', 'port', 'username','password','hostname')

    def __getitem__(self, item):   
        '''内置方法, 当使用obj['name']的形式的时候, 将调用这个方法, 这里返回的结果就是值'''
        return getattr(self, item)

    class Meta:
        verbose_name = '所有主机'
        verbose_name_plural = verbose_name






