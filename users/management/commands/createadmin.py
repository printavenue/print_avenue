from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from users.models import User


class Command(BaseCommand):
    help = "Crate superuser using email and password"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("email", nargs=1, type=str)
        parser.add_argument("password", nargs=1, type=str)
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> None:
        email = options["email"][0]
        password = options["password"][0]
        user = User.objects.create(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_admin = True
        user.is_moderator = True
        user.save()

        self.stdout.write(self.style.SUCCESS("Admin user created successfully."))
