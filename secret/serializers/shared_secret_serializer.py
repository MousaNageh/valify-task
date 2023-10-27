from user.serializers.user_serializer import UserSerializer
from rest_framework import serializers


class SharedSecretForUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserSerializer()


class SharedSecretSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    secret = serializers.CharField(source="secret.secret")
    shared_by = UserSerializer(source="secret.user")
