from django.contrib import admin
from secret.models import Secret, SharedSecret
from secret.crypto.secret_crypto import SecretCrypto


class SharedSecretInline(admin.StackedInline):
    model = SharedSecret
    readonly_fields = ["created_at"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user")


@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = ["user", "original_secret", "secret"]
    list_select_related = ["user"]
    search_fields = ["user__full_name", "user__email"]
    inlines = [SharedSecretInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["user", "secret", "original_secret", "created_at"]
        return ["created_at"]

    @staticmethod
    def original_secret(secret):
        if secret.secret:
            return SecretCrypto.decrypt_secret(secret.secret)
