from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.mixins import CreateModelMixin,ListModelMixin,DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from users.serializers import UserTokenSerializer
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny


User = get_user_model()


class UserLogin(APIView):
    def post(self, request):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        user = User.objects.all()[0]
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response(token)


class UserTokenViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):

    """
    登录
    """
    serializer_class = UserTokenSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = [AllowAny,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        pre_pwd = data['password']
        username = data['username']

        user = authenticate(username=username, password=pre_pwd)
        if user:
            login(request,user)
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False})

    def destroy(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

        #
        # try:
        #     user = User.objects.filter(username=username)[0]
        # except:
        #     return Response('用户不存在!', status=status.HTTP_400_BAD_REQUEST)
        #
        # if not check_password(pre_pwd, user.password):
        #     return Response('密码错误!', status=status.HTTP_400_BAD_REQUEST)
        # # 补充生成记录登录状态的token
        # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # payload = jwt_payload_handler(user)
        # token = jwt_encode_handler(payload)
        # headers = self.get_success_headers(serializer.data)
        # return Response(token, status=status.HTTP_200_OK, headers=headers)

#
class UsersViewSet(CreateModelMixin, GenericViewSet):
    """
    创建用户
    """
    serializer_class = UserTokenSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        login(request,user)
        return Response(token, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self,serializer):
        username = serializer.data['username']
        password = serializer.data['password']
        user = User.objects.create_user(username=username, password=password)
        return user


from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
# def UsersgininViewSite(request):
#     '''
#     用户登录
#     :param request:
#     :return:
#     '''
#     if request.method =="GET":
#         return render(request, 'user-login.html')
#     if request.method == 'POST':
#
#         user = request.POST.get('username')
#         password = request.POST.get('password')
#
#         User = get_user_model()
#         user = User.objects.get(user=user, password=password)
#         username = user.user
#
#         print(username)
#
#         # return render(request, 'user-index.html',{'username':username})
#         return JsonResponse({'username':username})


def UserloginViewSite(request):
    '''
    用户注册
    :param request:
    :return:
    '''

    return render(request, "user-login.html")

def UserlogoutViewSite(request):
    '''
    用户注销
    :param request:
    :return:
    '''
    logout(request)

    return render(request, "user-index.html")


def UsermakeViewSite(request):
    '''
    用户注册
    :param request:
    :return:
    '''

    return render(request, "user-make.html")


def UserindexViewSite(request):
    '''
    用户主页
    :param request:
    :return:
    '''

    return render(request, "user-index.html")


def UseraddcmpViewSite(request):
    '''
    用户添加主机
    :param request:
    :return:
    '''

    return render(request, "user-add-C.html")


def CremoteViewSite(request):
    '''
    用户远程查询
    :param request:
    :return:
    '''

    return render(request, "C-RemoteQuery.html")


def CmageViewSite(request):
    '''
    电脑详细信息
    :param request:
    :return:
    '''

    return render(request, "C-mage.html")


def CaddappViewSite(request):
    '''
    电脑详细信息
    :param request:
    :return:
    '''

    return render(request, "C-add-this.html")
