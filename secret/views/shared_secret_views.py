from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from secret.serializers.shared_secret_serializer import SharedSecretSerializer
from rest_framework.permissions import IsAuthenticated
from secret.queryset.shared_secret_queryset import SharedSecretQueryset
from secret.crypto.secret_crypto import SecretCrypto


class SharedSecretListAPI(ListAPIView):
    serializer_class = SharedSecretSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SharedSecretQueryset.get_shared_secrets_for_user(user=self.request.user)


class DecryptSharedSecret(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, shared_secret_id):
        shared_secret = SharedSecretQueryset.get_shared_secret_by_id_and_user(
            user=request.user, shared_secret_id=shared_secret_id
        )
        if not shared_secret:
            return Response(
                {"not_exist": f"shared secret with id {shared_secret_id} not exists ,"},
                status=HTTP_404_NOT_FOUND,
            )
        return Response(
            {"secret": SecretCrypto.decrypt_secret(shared_secret.secret.secret)},
            status=HTTP_200_OK,
        )
