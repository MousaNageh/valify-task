from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email = serializers.EmailField()
