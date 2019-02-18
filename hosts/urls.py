from django.conf.urls import url, include
from rest_framework import routers
from hosts.views import HostViewSet, play_book,ad_hoc


router = routers.DefaultRouter()
router.register(r'hosts', HostViewSet)
# router.register(r'host', HostloginViewSet)


urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^playbook/', play_book, name='play_book'),
    url(r'adhoc/', ad_hoc, name='ad_hoc'),


]