from rest_framework import serializers

from secret.validators.create_secret_validator import SharedSecretValidator


class ShareSecretWithUsersSerializer(serializers.Serializer):
    secret_id = serializers.IntegerField()
    shared_with = serializers.ListSerializer(
        child=serializers.EmailField(), allow_empty=False
    )

    def validate(self, attrs):
        if attrs.get("shared_with"):
            validator = SharedSecretValidator(
                user_emails=attrs.get("shared_with"),
                user=self.context.get("user"),
                secret_id=attrs.get("secret_id"),
            )
            attrs["shared_with"] = validator.validated_emails
            attrs["secret"] = validator.secret
        return attrs