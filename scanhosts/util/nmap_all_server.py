import os
import re

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))


import time
from scanhosts.lib.J_do import J_ssh_do
from scanhosts.lib.utils import mac_trans, sn_trans
from hosts.models import Host
from scanhosts.lib.utils import prpcrypt
from scanhosts.lib.utils import getsysversion


def snmp_begin(s_ownip, s_net, s_port, s_user, s_key, s_cmds):
    if not s_net:
        return False

    nm_item = NmapDev([])
    canlogin_list, notlogin_list = nm_item.try_login(s_net,s_port,s_user,s_key, s_cmds)
    crpt_do = prpcrypt()

    if canlogin_list:
        for item in canlogin_list:
            # crpt_pass = crpt_do.encrypt(canlogin_list[item][1]) if len(canlogin_list[item][1]) != 32 else \
            # canlogin_list[item][1]
            list = Host.objects.filter(hostip=s_net)
            for i in list:
                i.hostip = item
                i.port = str(canlogin_list[item][0])
                i.password = s_key
                i.username = canlogin_list[item][2]
                i.ssh_status = 1
                i.system_ver = canlogin_list[item][3] if canlogin_list[item][3] else "未获取"
                i.host_name = canlogin_list[item][4] if canlogin_list[item][4] else "未获取"
                i.mac_address = canlogin_list[item][5] if canlogin_list[item][5] else "未获取"
                i.sn = canlogin_list[item][6] if canlogin_list[item][6] else "请使用root用户登录获取"
                i.save()

    if notlogin_list:
        list = Host.objects.filter(hostip=s_net)
        try:
            for i in list:
                i.ssh_status = 0
                i.save()
        except Exception as e:
            print(e)
            x = 1
class NmapDev(object):
    '''
    扫描类：扫描获取指定ip对象信息
    '''

    def __init__(self, black_list=[]):
        self.black_list = black_list
        self.can_login_lst = {}
        self.not_login_lst = {}

    def try_login(self, s_net, s_port, s_user, s_key, s_cmds):
        '''
        尝试ssh用户密码登录，获取机器基本信息
        :param sship_list:
        :param password_list:
        :param syscmd_list:
        :return:
        '''

        login_info = [s_net, int(s_port), s_user, s_key]
        doobj = J_ssh_do(login_info)
        res = doobj.pass_do(login_info, s_cmds)
        if res["status"] == "success":
            print('11111111111')
            if s_net in self.not_login_lst:
                self.not_login_lst.pop(s_net)
            sys_hostname = res["hostname"]
            sys_mac = mac_trans(
                res["cat /sys/class/net/[^vtlsb]*/address||esxcfg-vmknic -l|awk '{print $8}'|grep ':'"])
            sys_sn = sn_trans(res["dmidecode -s system-serial-number"])
            system_info = getsysversion([res["cat /etc/issue"], res["cat /etc/redhat-release"]])
            self.can_login_lst[s_net] = (
            s_port, s_key, s_user, system_info, sys_hostname, sys_mac, sys_sn)
        elif res["status"] == "failed" and re.search(r"reading SSH protocol banner", res["res"]):
            print("2222222222222")
            print("IP:%s Connection closed by remote host,Sleep 0.1 (s).................. " % s_net, res)
            time.sleep(0.1)
        else:
            if s_net not in self.not_login_lst.keys() and s_net not in self.can_login_lst.keys():
                print("33333333333")
                self.not_login_lst[s_net] = s_port

        return self.can_login_lst, self.not_login_lst
