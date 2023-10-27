from django.urls import path

from user.views.user_view import LoginView, RegisterView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("login", LoginView.as_view(), name="user-login"),
    path("register", RegisterView.as_view(), name="user-register"),
    path(
        "refresh-token",
        jwt_views.TokenRefreshView.as_view(),
        name="user-refresh-token",
    ),
]
