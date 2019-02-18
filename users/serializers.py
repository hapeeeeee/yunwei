from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'password')
