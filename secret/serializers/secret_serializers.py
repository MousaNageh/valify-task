from rest_framework import serializers
from secret.crypto.secret_crypto import SecretCrypto
from secret.serializers.shared_secret_serializer import SharedSecretForUserSerializer


class SecretSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    secret = serializers.SerializerMethodField()
    shared_with = SharedSecretForUserSerializer(source="shared_secrets", many=True)

    @staticmethod
    def get_secret(secret):
        return SecretCrypto.decrypt_secret(secret.secret)
