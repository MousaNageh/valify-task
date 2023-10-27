from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.querysets.user_queryset import UserQueryset
from user.validators.password import PasswordChecker


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)
    re_password = serializers.CharField(min_length=8, max_length=68, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["full_name", "email", "password", "re_password"]

    def validate(self, attrs):
        PasswordChecker.password_serializer_validator(
            password=attrs.get("password"), re_password=attrs.get("re_password")
        )
        return attrs

    def create(self, validated_data):
        # remove re_password from validated data
        del validated_data["re_password"]
        # add is_active to validated data
        validated_data["is_active"] = True

        return UserQueryset.create_user(**validated_data)
