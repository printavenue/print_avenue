from typing import Union

from django.contrib.auth.hashers import check_password
from django.db.models import Q

from users.models import User


class EmailPhoneUsernameAuthenticationBackend(object):
    @staticmethod
    def authenticate(request, username=None, password=None) -> Union[User, None]:
        try:
            user = User.objects.get(Q(phone_number=username) | Q(email=username))

        except User.DoesNotExist:
            return None

        if user and check_password(password, user.password):
            return user

        return None

    @staticmethod
    def get_user(user_id: int) -> Union[User, None]:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
