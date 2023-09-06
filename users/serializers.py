from typing import Any, Dict

from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import RegexValidator
from django.urls import reverse

from rest_framework import serializers
from users.constants import PHONE_NUMBER_REGEX
from users.models import User
from users.tasks import send_activation_email
from users.tokens import AccountActivationTokenGenerator
from users.validators import is_empty, is_valid_email, is_valid_phone_number


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_username(self, username):
        if not (is_valid_email(username) or is_valid_phone_number(username)):
            raise serializers.ValidationError(
                "username is not a valid email address or phone number"
            )
        return username


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=True)
    phone_number = serializers.CharField(
        allow_blank=True,
        validators=[RegexValidator(PHONE_NUMBER_REGEX, "Enter a valid phone number.")],
    )
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: Any) -> Any:
        data = super().validate(attrs)
        if is_empty(data.get("email", "")) and is_empty(data.get("phone_number", "")):
            raise serializers.ValidationError("Email address or phone number is required.")
        user_name_field = "phone_number"
        if not is_empty(data.get("email", "")):
            user_name_field = "email"
            user = User.objects.filter(email=data["email"])
        else:
            user = User.objects.filter(phone_number=data["phone_number"])

        if user.exists():
            raise serializers.ValidationError(
                {user_name_field: "User with this {} already exists.".format(user_name_field)}
            )
        return attrs

    def create(self, validated_data: Dict[str, str]) -> User:
        user = User.objects.create(
            email=validated_data.get("email", ""),
            phone_number=validated_data.get("phone_number", ""),
        )
        user.set_password(validated_data["password"])
        user.save()

        account_activation_token = AccountActivationTokenGenerator()
        token = account_activation_token.make_token(user)
        current_site = get_current_site(self.context.get("request")).domain
        relativeUrl = reverse(
            "activate_account", kwargs={"token": token, "identifier": user.identifier}
        )
        absoluteUrl = f"http://{current_site}/{relativeUrl}".format(current_site, relativeUrl)

        if validated_data.get("email", ""):
            send_activation_email.delay(validated_data.get("email"), absoluteUrl)
        return user
