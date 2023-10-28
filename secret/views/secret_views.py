from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from secret.serializers.create_secret_serializer import CreateSecretSerializer
from secret.queryset.secret_queryset import SecretQueryset
from secret.serializers.secret_serializers import SecretSerializer
from secret.crypto.secret_crypto import SecretCrypto


class SecretAPIView(CreateAPIView, ListAPIView):
    serializer_class = SecretSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SecretQueryset.get_user_secrets(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = CreateSecretSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        created_secret = SecretQueryset.create_secret_with_shared_secrets(
            user=request.user,
            secret=serializer.validated_data.get("secret"),
            shared_with_emails=serializer.validated_data.get("shared_with"),
        )
        return Response(
            {
                "id": created_secret.id,
                "secret": SecretCrypto.decrypt_secret(created_secret.secret),
            },
            status=HTTP_201_CREATED,
        )
