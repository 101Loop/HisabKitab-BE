import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from faker import Faker

from users.models import AuthTransaction, OTPValidation

User = get_user_model()

faker = Faker()


def generate_random_mobile():
    return str(faker.random_int(min=6, max=9)) + str(
        faker.random_number(digits=9, fix_len=True)
    )


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: faker.user_name() + str(n))
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.LazyFunction(lambda: make_password(faker.password()))
    name = factory.LazyAttribute(lambda o: faker.name())
    mobile = factory.LazyFunction(generate_random_mobile)
    is_active = True


class AuthTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AuthTransaction

    user = factory.SubFactory(UserFactory)
    ip_address = factory.LazyFunction(lambda: faker.ipv4())


class OTPValidationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OTPValidation

    otp = factory.LazyFunction(lambda: faker.random_number(digits=6, fix_len=True))
    type = "email"
