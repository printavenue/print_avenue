from typing import Iterable
from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import force_str

from pa_commons.models import PABaseModel
from users.constants import PHONE_NUMBER_REGEX

# Create your models here.


class UserManager(BaseUserManager["User"]):
    def create_user(self, email, phone_number, password=None) -> "User":
        if not email or not phone_number:
            raise ValidationError("Both Email and Phone Numer can't be empty.")
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None) -> "User":
        if not email:
            raise ValidationError("Email can't be empty.")

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.is_admin = True
        user.is_moderator = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, PABaseModel):
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
        validators=[RegexValidator(PHONE_NUMBER_REGEX, "Invalid phone number")],
    )
    is_admin = models.BooleanField("Is Admin", default=False)
    is_moderator = models.BooleanField("Is Moderator", default=False)

    objects = UserManager()

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
        self.full_clean()
        if not self.email and not self.phone_number:
            raise ValidationError("Both Email and Phone Numer can't be empty.")

        return super().save(force_insert, force_update, using, update_fields)
