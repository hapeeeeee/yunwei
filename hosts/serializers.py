from rest_framework import serializers
from hosts.models import Host

class HostCreateSerializers(serializers.ModelSerializer):
    hostowner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Host
        fields = ('hostowner','hostip', 'port','username','password','hostname')


class HostReadSerializers(serializers.ModelSerializer):

    class Meta:
        model = Host
        fields = ('id','hostip', 'port','username','password','hostowner')


class HostUpdateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Host
        fields = ('hostip', 'port','username','password')


from hosts.models import *
from rest_framework import serializers


class HostLoginifoSerializer(serializers.ModelSerializer):
    hostowner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Host
        fields = "__all__"