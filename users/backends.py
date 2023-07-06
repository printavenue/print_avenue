from typing import Union

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from users.models import User as CustomUser

User = get_user_model()


class EmailPhoneUsernameAuthenticationBackend(object):
    @staticmethod
    def authenticate(request, username=None, password=None) -> Union[CustomUser, None]:
        try:
            user = CustomUser.objects.get(Q(phone_number=username) | Q(email=username))

        except CustomUser.DoesNotExist:
            return None

        if user and check_password(password, user.password):
            return user

        return None

    @staticmethod
    def get_user(user_id: int) -> Union[CustomUser, None]:
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
