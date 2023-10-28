from rest_framework import serializers
from secret.validators.create_secret_validator import SharedSecretValidator


class CreateSecretSerializer(serializers.Serializer):
    secret = serializers.CharField(min_length=8)
    shared_with = serializers.ListSerializer(
        child=serializers.EmailField(), allow_empty=True
    )

    def validate(self, attrs):
        if attrs.get("shared_with"):
            attrs["shared_with"] = SharedSecretValidator(
                user_emails=attrs.get("shared_with"), user=self.context.get("user")
            ).validated_emails
        return attrs



