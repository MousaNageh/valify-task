from django.urls import path
from secret.views.secret_views import SecretAPIView
from secret.views.shared_secret_views import (
    SharedSecretListAPI,
    DecryptSharedSecret,
    ShareSecretWithUsersView,
)

urlpatterns = [
    path("", SecretAPIView.as_view(), name="secret-api"),
    path(
        "share-with", ShareSecretWithUsersView.as_view(), name="secret-share-with-api"
    ),
    path("shared", SharedSecretListAPI.as_view(), name="shared-secret-list-api"),
    path(
        "shared/<int:shared_secret_id>",
        DecryptSharedSecret.as_view(),
        name="shared-secret-decrypt-api",
    ),
]
