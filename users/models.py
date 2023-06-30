from typing import Iterable
from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import force_str

from pa_commons.models import PABaseModel
from users.constants import PHONE_NUMBER_REGEX

# Create your models here.


class User(AbstractBaseUser, PABaseModel):
    identifier = models.UUIDField(
        "Identifier", unique=True, db_index=True, editable=False, default=uuid4
    )
    email = models.EmailField("Email", max_length=255, unique=True, blank=True, null=True)
    phone_number = models.CharField(
        "Phone Number",
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(PHONE_NUMBER_REGEX, "Invalid Phone Number")],
    )
    is_admin = models.BooleanField("Is Admin", default=False)
    is_moderator = models.BooleanField("Is Moderator", default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return force_str(self.identifier)

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        if not self.email and not self.phone_number:
            raise ValidationError("Both Email and Phone Numer can't be empty.")
        return super().save(force_insert, force_update, using, update_fields)
