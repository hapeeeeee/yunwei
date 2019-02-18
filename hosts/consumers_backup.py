from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import asyncio
import time
import random


class ChatConsumer(WebsocketConsumer):
    """
    异步的socket消费者，调试用
    """
    def get_host_info(self):
        """
        获取所有远程主机的状态
        :return: data_dicts
        """
        hosts = []
        hostnames = []
        all_hosts = Host.objects.all()
        for host in all_hosts:
            host = dict(host)
            hosts.append(host)
            hostnames.append(host['hostname'])

        resource = dict()

        resource['test'] = dict()
        resource['test']['hosts'] = hosts

        rbt = ANSRunner(resource)

        # rbt.run_model(host_list=[hostname, ], module_name='ping', module_args="")
        rbt.run_model(host_list=hostnames, module_name='setup', module_args="filter=ansible_*_mb")
        data_dicts = rbt.get_model_result()
        return data_dicts

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        # 发送数据给前端 hostowner_id host_name hostip port username system_ver ssh_status mac_address res_freememory res_allmemory
        while True:

            data_dicts = self.get_host_info()
            msg_objects_list = []
            ssh_map = {0: '连接异常', 1: '已连接'}
            for data_key in data_dicts:
                for hostname in data_dicts[data_key]:
                    hostname = hostname.replace('_', '.')
                    host = Host.objects.filter(hostname=hostname)[0]
                    hostname = hostname.replace('.', '_')
                    host_name = host.host_name
                    hostip = host.hostip
                    port = host.port
                    hostowner_id = host.hostowner_id
                    username = host.username
                    system_ver = host.system_ver
                    ssh_status_num = host.ssh_status
                    ssh_status = ssh_map.get(ssh_status_num)
                    mac_address = host.mac_address
                    message = {"hostowner_id": hostowner_id, "host_name": host_name, "hostip": hostip, "port": port,
                               "username": username,
                               "system_ver": system_ver, "ssh_status": ssh_status,
                               "mac_address": mac_address, "res_freememory": '未获取', "res_allmemory": "未获取"}
                    # 扫描主机硬件信息
                    from utils.scan_hosts import scan_hosts
                    scan_hosts()

                    # 筛选可以远程连接的主机的数据
                    if data_key == "success":
                        try:
                            res_freememory = data_dicts['success'][hostname]['ansible_facts']['ansible_memfree_mb']

                            res_allmemory = data_dicts['success'][hostname]['ansible_facts']['ansible_memtotal_mb']

                            message.update({"res_freememory": res_freememory, "res_allmemory": res_allmemory})

                            # message["res_freememory"]=res_freememory
                            # message["res_allmemory"]=res_allmemory
                            print('-----------------获取内存成功--------------------')

                        except Exception as e:
                            print(e, '--------获取远程信息异常-------')
                            print(message)

                        finally:
                            msg_objects_list.append(message)

                            print('--------登录主机状态获取成功------------')
                    # 筛选可以远程连接的主机的数据
                    else:
                        msg_objects_list.append(message)
                        print('--------未登录主机状态获取成功------------')
                    # 控制扫描时间
                    asyncio.sleep(1)

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': msg_objects_list
                }
            )

            # self.send(text_data=json.dumps({
            #     'message': msg_objects_list
            # }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # # Receive message from WebSocket
    # def receive(self, text_data):
    #     print('-----------------------------')
    #     text_data_json = json.loads(text_data)
    #     message_web = text_data_json['message']
    #     print(message_web)
    #     for i in range(1000):
    #         l=['老王','老李','机器猫','钢铁侠']
    #         message=random.choice(l)+str(i)
    #
    #         # Send message to room group
    #         async_to_sync(self.channel_layer.group_send)(
    #             self.room_group_name,
    #             {
    #                 'type': 'chat_message',
    #                 'message': message
    #             }
    #         )
    #         asyncio.sleep(0.1)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket

        self.send(text_data=json.dumps({
            'message': message

        }
        ))
        asyncio.sleep(0.01)


# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from taskdo.utils.base.ansible_api import ANSRunner
from hosts.models import Host
from django_redis import get_redis_connection


# /C-mage.html
class ChatConsumer1(WebsocketConsumer):
    """
    同步代码
    从用户远程服务器上获取参数，并通过socket返回给前端
    :param None
    :return socket_msg
                            { "hostowner_id": hostowner_id, "host_name": host_name, "hostip": hostip, "port": port,
                               "username": username,"system_ver": system_ver, "ssh_status": ssh_status,
                               "mac_address": mac_address, "res_freememory": '未获取', "res_allmemory": "未获取"}
    """
    def get_host_info(self):
        """
        获取所有远程主机的状态
        :return: data_dicts
        """
        hosts = []
        hostnames = []
        all_hosts = Host.objects.all()
        for host in all_hosts:
            host = dict(host)
            hosts.append(host)
            hostnames.append(host['hostname'])

        resource = dict()

        resource['test'] = dict()
        resource['test']['hosts'] = hosts

        rbt = ANSRunner(resource)

        # rbt.run_model(host_list=[hostname, ], module_name='ping', module_args="")
        rbt.run_model(host_list=hostnames, module_name='setup', module_args="filter=ansible_*_mb")
        data_dicts = rbt.get_model_result()
        return data_dicts


    def connect(self):
        """
        接收前段的socket连接，并发送消息给前端的socket
        :return: socket_msg
        """
        #服务端，接收数据
        self.accept()
        # 发送数据给前端 hostowner_id host_name hostip port username system_ver ssh_status mac_address res_freememory res_allmemory
        while True:

            data_dicts=self.get_host_info()
            msg_objects_list = []
            ssh_map = {0: '连接异常', 1: '已连接'}
            for data_key in data_dicts:
                for hostname in data_dicts[data_key]:
                    hostname = hostname.replace('_', '.')
                    host = Host.objects.filter(hostname=hostname)[0]
                    hostname = hostname.replace('.', '_')
                    host_name = host.host_name
                    hostip = host.hostip
                    port = host.port
                    hostowner_id = host.hostowner_id
                    username = host.username
                    system_ver = host.system_ver
                    ssh_status_num = host.ssh_status
                    ssh_status = ssh_map.get(ssh_status_num)
                    mac_address = host.mac_address
                    message = {"hostowner_id": hostowner_id, "host_name": host_name, "hostip": hostip, "port": port,
                               "username": username,
                               "system_ver": system_ver, "ssh_status": ssh_status,
                               "mac_address": mac_address, "res_freememory": '未获取', "res_allmemory": "未获取"}
                    #扫描主机硬件信息
                    from utils.scan_hosts import scan_hosts
                    scan_hosts()

                    #筛选可以远程连接的主机的数据
                    if data_key == "success":
                        try:
                            res_freememory = data_dicts['success'][hostname]['ansible_facts']['ansible_memfree_mb']

                            res_allmemory = data_dicts['success'][hostname]['ansible_facts']['ansible_memtotal_mb']

                            message.update({"res_freememory": res_freememory, "res_allmemory": res_allmemory})

                            # message["res_freememory"]=res_freememory
                            # message["res_allmemory"]=res_allmemory
                            print('-----------------获取内存成功--------------------')

                        except Exception as e:
                            print(e, '--------获取远程信息异常-------')
                            print(message)

                        finally:
                            msg_objects_list.append(message)
                            # Send message to web

                            self.send(text_data=json.dumps({
                                'message': msg_objects_list
                            }))
                            print('--------登录主机状态获取成功------------')
                    #筛选可以远程连接的主机的数据
                    else:
                        msg_objects_list.append(message)
                        self.send(text_data=json.dumps({
                            'message': msg_objects_list
                        }))
                        print('--------未登录主机状态获取成功------------')
                    #控制扫描时间
                    time.sleep(0.1)

    def disconnect(self, close_code):
        """
        关闭socket
        :param close_code:
        :return:
        """
        self.close(close_code)

    def receive(self, text_data):
        """
        接收socket客服端发送的消息
        :param text_data:
        :return:
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

    #发送消息给对应socket
    # self.send(text_data=json.dumps({
    #     'message': message
    # }))
