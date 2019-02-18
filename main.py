import os
import yaml

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

os.environ["DJANGO_SETTINGS_MODULE"] = 'yunwei.settings'
import django
django.setup()
from scanhosts.util.nmap_all_server import snmp_begin
from hosts.models import Host


def main():
    '''
    读取扫描所需配置文件
    :return:
    '''
    conns = Host.objects.all()
    s_conf = yaml.load(open('conf/scanhosts.yaml'))
    for conn in conns:
        s_ownip = conn.hostowner
        s_net = conn.hostip
        s_port = conn.port
        s_user = conn.username
        s_key = conn.password
        s_cmds = s_conf['hostsinfo']['syscmd_list']

        '''
        扫描主机信息
        '''
        snmp_begin(s_ownip, s_net, s_port, s_user, s_key, s_cmds)


if __name__ == "__main__":
    main()
