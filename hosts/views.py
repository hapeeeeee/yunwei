from django.shortcuts import render
from hosts.serializers import HostCreateSerializers, HostReadSerializers, HostUpdateSerializers, HostLoginifoSerializer
from rest_framework.viewsets import ModelViewSet
from taskdo.utils.base.ansible_api import ANSRunner
from hosts.models import Host
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework_extensions.cache.mixins import CacheResponseMixin
import json
from time import sleep
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.


# class HostloginViewSet(CacheResponseMixin, ModelViewSet):
#     """
#     list:
#         获取所有的机器信息
#     create:
#         添加单个机器信息
#     retrieve:
#         获取单个的机器信息
#     """
#     # queryset = MovieInfoSerializer.Meta.model.objects.all()
#     # queryset 指明该视图集在查询数据时使用的查询集
#     # serializer_class 指明该视图在进行序列化或反序列化时使用的序列化器
#     serializer_class = HostLoginifoSerializer
#     queryset = serializer_class.Meta.model.objects.all()
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class HostViewSet(ModelViewSet):
    '''
    create:
        添加一台主机信息，点击添加后，测试是否能够连接，返回连接结果（false、true）
    '''
    serializer_class = HostReadSerializers
    queryset = serializer_class.Meta.model.objects.all()
    authentication_classes = [SessionAuthentication,]
    permission_classes = [AllowAny,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return HostReadSerializers
        if self.action in ('create',):
            return HostCreateSerializers

        if self.action in ('update', 'partial_update'):
            return HostUpdateSerializers

    def get_queryset(self):
        user = self.request.user
        return HostLoginifoSerializer.Meta.model.objects.filter(hostowner=user)

    def perform_create(self, serializer):
        all_username = serializer.data['username'].split(',')
        all_password = serializer.data['password'].split(',')
        all_hostname = serializer.data['hostname'].split(',')
        all_ip = serializer.data['hostip'].split(',')
        all_port = serializer.data['port'].split(',')

        hosts = []
        for i in range(len(all_ip)):
            host = {'username': all_username[i], 'password': all_password[i], 'ip': all_ip[i], 'port': all_port[i], 'hostname': all_hostname[i]}
            hosts.append(host)



        for i in range(len(all_ip)):

            Host.objects.create(username=all_username[i],password=all_password[i],hostip=all_ip[i],
                                port=all_port[i], hostname=all_hostname[i], hostowner=self.request.user)

        data = self.host_test(serializer, hosts, all_hostname)
        return data

    def host_test(self, serializer, hosts, all_hostname):
        x = 1
        # all_username = serializer.data['host_username'].split(',')
        # all_password = serializer.data['host_password'].split(',')
        # all_hostname = serializer.data['hostname'].split(',')
        # all_ip = serializer.data['hostip'].split(',')
        # all_port = serializer.data['hostport'].split(',')

        # hosts = []
        # for i in range(len(all_ip)):
        #     host = {'username': all_username[i], 'password': all_password[i], 'ip': all_ip[i], 'port': all_port[i], 'hostname': all_hostname[i]}
        #     hosts.append(host)

        resource = dict()

        resource['test'] = dict()
        resource['test']['hosts'] = hosts

        rbt = ANSRunner(resource)

        # rbt.run_model(host_list=[hostname, ], module_name='ping', module_args="")
        rbt.run_model(host_list=all_hostname, module_name='ping', module_args="")

        data = rbt.get_model_result()


        return data


# class HostTopViewSet(ModelViewSet):
#     serializer_class = HostTopSerializers
#     queryset = serializer_class.Meta.model.objects.all()
#
#     def get_queryset(self):
#         user = self.request.user
#         return self.serializer_class.Meta.model.objects.filter(hostowner=user)


# def nginx_install(request):
#     username = request.POST['host_username']
#     password = request.POST['host_password']
#     hostname = request.POST['hostname']
#     ip = request.POST['hostip']
#     port = request.POST['hostport']
#
#     host = {'username': username, 'password': password, 'ip': ip, 'port': port, 'hostname': hostname}
#     hosts = [host, ]
#
#     resource = dict()
#
#     resource['test'] = dict()
#     resource['test']['hosts'] = hosts
#
#     rbt = ANSRunner(resource)
#
#     rbt.run_playbook(playbook_path='../yunwei/taskdo/utils/base/install_nginx')
#     data = rbt.get_playbook_result()
#     print(data)

def make_resource(hosts):
    resource = dict()
    resource['test'] = dict()
    resource['test']['hosts'] = []

    for hostip in hosts:
        host = Host.objects.filter(hostip=hostip)[0]
        host_dict = dict(host)
        resource['test']['hosts'].append(host_dict)

    return resource


def play_book(request):
    '''
    /hosts/playbook

    前端为两个复选框，
    第一个复选框是主机复选框，传值为主机的ip
    第二个复选框 是需要安装的环境

    :param request:
    :return:
    '''
    hosts = request.POST.getlist('host[]')
    installs = request.POST.getlist('install[]')
    resource = make_resource(hosts)
    rbt = ANSRunner(resource)
    res = dict()

    for insta in installs:
        playbook_path = '../pycharm_project_205/taskdo/utils/base/install_' + insta

        rbt.run_playbook(playbook_path=playbook_path)
        data = rbt.get_playbook_result()
        res[insta] = data

    return JsonResponse(res)


# from hosts.serializers import TaskSerializers
# class TaskViewSet(ModelViewSet):
#     serializer_class = TaskSerializers
#     queryset = Host.objects.all()


    # def get_queryset(self):
    #     user = self.request.user
    #     return Host.objects.filter(hostowner=user)


def ad_hoc(request):
    '''
    /hosts/adhoc
    前端为一个复选框和一个输入框
    复选框是用户主机，传值为主机ip
    输入框为输入的命令，如：'ls /'

    :param request:
    :return:
    '''
    hosts = request.POST.getlist('host[]')
    module_args = request.POST['module_args']

    resource = make_resource(hosts)
    rbt = ANSRunner(resource)

    rbt.run_model(host_list=hosts,module_name='shell',module_args=module_args)
    res = rbt.get_model_result()

    # data = dict()
    # success_hosts = res['success'].keys()
    # unreach_hosts = res['unreachable'].keys()
    # failed_hosts = res['failed'].keys()
    #
    # for success_host in success_hosts:
    #     data[success_host] = res['success'][success_host]['stdout']
    #
    # for failed_host in failed_hosts:
    #     data[failed_host] = res['failed'][failed_host]['stderr']
    #
    # for unreach_host in unreach_hosts:
    #     data[unreach_host] = res['unreachable'][unreach_host]['msg']
    return JsonResponse(res)
# /user/login





