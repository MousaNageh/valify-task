from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import LoginSerializer, RegisterSerializer


class LoginView(TokenObtainPairView):
    permission_classes = []
    authentication_classes = []
    serializer_class = LoginSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
