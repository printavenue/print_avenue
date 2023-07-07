# Generated by Django 4.2.2 on 2023-06-30 08:44

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(blank=True, null=True, verbose_name="last login"),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "identifier",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.UUID("2383dfe7-3462-47c4-ba88-50c5e0a64f5d"),
                        editable=False,
                        unique=True,
                        verbose_name="Identifier",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="Email",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^(\\+?\\d{0,4})?\\s?-?\\s?(\\(?\\d{3}\\)?)\\s?-?\\s?(\\(?\\d{3}\\)?)\\s?-?\\s?(\\(?\\d{4}\\)?)?$",
                                "Invalid Phone Number",
                            )
                        ],
                        verbose_name="Phone Number",
                    ),
                ),
                (
                    "is_admin",
                    models.BooleanField(default=False, verbose_name="Is Admin"),
                ),
                (
                    "is_moderator",
                    models.BooleanField(default=False, verbose_name="Is Moderator"),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
        ),
    ]
