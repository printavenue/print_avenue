import pytest
from users.backends import EmailPhoneUsernameAuthenticationBackend

pytestmark = pytest.mark.django_db

USER_DATA = [
    "test@gmail.com",
    "+251926600549",
    "superstrongpassword",
]


@pytest.fixture
def setup_user(user_factory):
    user = user_factory(
        email=USER_DATA[0],
        phone_number=USER_DATA[1],
    )
    user.set_password(USER_DATA[2])
    user.save()


def test_backend_authenticated_valid_user_email_and_password(setup_user, rf):
    user = EmailPhoneUsernameAuthenticationBackend.authenticate(rf, USER_DATA[0], USER_DATA[2])
    assert user
    assert user.email == USER_DATA[0]


def test_backend_authenticated_valid_user_phone_number_and_password(setup_user, rf):
    user = EmailPhoneUsernameAuthenticationBackend.authenticate(rf, USER_DATA[1], USER_DATA[2])
    assert user
    assert user.phone_number == USER_DATA[1]


def test_backend_returns_none_for_valid_email_and_invalid_password(setup_user, rf):
    user = EmailPhoneUsernameAuthenticationBackend.authenticate(rf, USER_DATA[0], "DUMMY")
    assert not user


def test_backend_returns_none_for_invalid_email_and_valid_password(setup_user, rf):
    user = EmailPhoneUsernameAuthenticationBackend.authenticate(rf, "DUMMY", USER_DATA[2])
    assert not user
