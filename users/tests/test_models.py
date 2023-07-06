from django.core.exceptions import ValidationError

import pytest
from users.models import User

pytestmark = pytest.mark.django_db

USER_DATA = [
    "test@gmail.com",
    "+251926600549",
]


@pytest.fixture
def setup_user_data(user_factory):
    user_factory(
        email=USER_DATA[0],
        phone_number=USER_DATA[1],
    )


def test_user_model_create_user_successfully(user_factory):
    before_count = User.objects.count()
    user = user_factory()
    user.save()
    after_count = User.objects.count()
    assert user.email
    assert user.phone_number
    assert after_count == before_count + 1


def test_user_model_create_user_with_only_email(user_factory):
    before_count = User.objects.count()
    user = user_factory(email=USER_DATA[0], phone_number="")
    user.save()
    after_count = User.objects.count()
    assert user.email == USER_DATA[0]
    assert not user.phone_number
    assert after_count == before_count + 1


def test_user_model_create_user_with_phone_number_only(user_factory):
    before_count = User.objects.count()
    user = user_factory(email="", phone_number=USER_DATA[1])
    user.save()
    after_count = User.objects.count()
    assert user.phone_number == USER_DATA[1]
    assert not user.email
    assert after_count == before_count + 1


def test_user_model_create_user_raises_error_for_invalid_email(user_factory):
    with pytest.raises(ValidationError, match=r"Enter a valid email address."):
        user_factory(email="DUMMY")


def test_user_model_create_user_raises_error_for_invalid_phone_number(user_factory):
    with pytest.raises(ValidationError, match=r"Invalid phone number"):
        user_factory(phone_number="DUMMY")


def test_user_model_create_raises_error_when_both_email_and_phone_number_is_missing(user_factory):
    with pytest.raises(ValidationError, match=r"Both Email and Phone Numer can\'t be empty."):
        user_factory(phone_number="", email="")


def test_user_model_create_raises_error_for_empty_password(user_factory):
    with pytest.raises(ValidationError, match=r"This field cannot be blank."):
        user_factory(password="")


def test_user_model_raises_error_for_duplicate_email(setup_user_data, user_factory):
    with pytest.raises(ValidationError, match=r"User with this Email already exists."):
        user_factory(email=USER_DATA[0])


def test_user_model_raises_error_for_duplicate_phone_number(setup_user_data, user_factory):
    with pytest.raises(ValidationError, match=r"User with this Phone Number already exists."):
        user_factory(phone_number=USER_DATA[1])
