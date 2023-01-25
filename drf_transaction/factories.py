import random
from django.utils import timezone
import factory
from django.contrib.auth import get_user_model
from faker import Faker

from drf_contact.factories import ContactDetailFactory
from users.factories import UserFactory
from drf_transaction.models import TransactionMode, TransactionDetail

User = get_user_model()

faker = Faker()


class TransactionModeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransactionMode

    mode = factory.LazyAttribute(lambda o: faker.name())
    created_by = factory.SubFactory(UserFactory)


class TransactionDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransactionDetail

    contact = factory.SubFactory(ContactDetailFactory)
    category = random.choice(["C", "D"])
    transaction_date = timezone.now()
    amount = factory.LazyAttribute(
        lambda o: faker.pyfloat(min_value=1, max_value=1000, positive=True)
    )
    mode = factory.SubFactory(TransactionModeFactory)
    created_by = factory.SubFactory(UserFactory)
