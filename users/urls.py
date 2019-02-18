from django.conf.urls import url, include
from users.views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('login', UserTokenViewSet)
router.register('register', UsersViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^userlogin/$', UserloginViewSite, name='login'),
    url(r'^userlogout/$', UserlogoutViewSite, name='logout'),
    url(r'^usermake/$', UsermakeViewSite, name='nake'),
    url(r'^addapp/', CaddappViewSite, name='addapp'),
    url(r'^putermage', CmageViewSite, name='putermage'),
    url(r'^remotquery', CremoteViewSite, name='remotquery'),
    url(r'^useraddputer/', UseraddcmpViewSite, name='addputer'),
    url(r'^index/$', UserindexViewSite, name='index'),
]

