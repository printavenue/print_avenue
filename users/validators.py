import re

from users.constants import EMAIL_REGEXT, PHONE_NUMBER_REGEX


def is_valid_email(email: str) -> bool:
    return bool(re.match(EMAIL_REGEXT, email))


def is_valid_phone_number(number: str) -> bool:
    return bool(re.match(PHONE_NUMBER_REGEX, number))


def is_empty(string: str) -> bool:
    return not bool(string)
