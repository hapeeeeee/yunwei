import os
import paramiko
from scanhosts.lib.utils import prpcrypt
os.environ["DJANGO_SETTINGS_MODULE"] = 'yunwei.settings'


class J_ssh_do(object):
    def __init__(self, info=""):
        self.whitelist = ["*"]
        self.result = {"info": info}

    def pass_do(self, login_info, cmd_list=""):
        '''
        用户密码方式登录
        :param login_info:登录的信息，如：('10.211.55.3', 22, 'parallels', 'xxx777')
        :param cmd_list:登录机器后，需要执行的命令
        :return:
        '''
        try:
            # transport = paramiko.Transport((login_info[0], login_info[1]))
            # print(transport.banner_timeout)
            # transport.banner_timeout = 30
            # print(transport.banner_timeout)


            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if len(login_info[3]) == 32:
                crpt_de = prpcrypt()
                pp= crpt_de.decrypt(login_info[3])
                login_info[3]= str(pp).split('\\')[0].split('\'')[-1]
            ssh.connect(login_info[0],login_info[1],login_info[2],login_info[3],timeout=3)
            self.result["status"] = "success"
            for cmd in cmd_list:
                stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
                std_res = stdout.read()
                self.result[cmd] = std_res
        except Exception as e:
            self.result["status"] = "failed"
            self.result["res"] = str(e)
        return self.result