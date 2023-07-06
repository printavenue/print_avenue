import factory
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    phone_number = factory.Sequence(lambda n: "+251{:09}".format(n))
    password = factory.Faker("password")
