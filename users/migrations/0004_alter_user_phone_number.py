# Generated by Django 4.2.3 on 2023-07-07 05:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_user_groups_user_is_superuser_user_user_permissions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^((\\+?\\d{0,4})?\\s?-?\\s?(\\(?\\d{3}\\)?)\\s?-?\\s?(\\(?\\d{3}\\)?)\\s?-?\\s?(\\(?\\d{4}\\)?)?)?$",
                        "Invalid phone number.",
                    )
                ],
                verbose_name="Phone Number",
            ),
        ),
    ]
