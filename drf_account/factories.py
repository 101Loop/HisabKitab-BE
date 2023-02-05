import random

import factory
from faker import Faker

from drf_account.models import BankAccount, BankMaster, Card, CreditCard, DebitCard
from users.factories import UserFactory

faker = Faker()


class BankMasterFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda o: faker.name())
    aliases = factory.LazyAttribute(lambda o: faker.json())

    class Meta:
        model = BankMaster


class BankAccountFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    nickname = factory.LazyAttribute(lambda o: faker.name())
    bank = factory.SubFactory(BankMasterFactory)
    description = factory.LazyAttribute(lambda o: faker.text())
    accnumber = factory.LazyAttribute(lambda o: faker.text())
    minbal = factory.LazyAttribute(lambda o: faker.pyint(min_value=1, max_value=1000))

    class Meta:
        model = BankAccount


class CreditCardFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    nickname = factory.LazyAttribute(lambda o: faker.name())
    bank = factory.SubFactory(BankMasterFactory)
    description = factory.LazyAttribute(lambda o: faker.text())
    account = factory.SubFactory(BankAccountFactory)
    vendor = factory.LazyAttribute(lambda o: random.choices(["V", "M", "MC"]))
    limit = factory.LazyAttribute(
        lambda o: faker.pyint(min_value=10000, max_value=50000)
    )
    statement_date = factory.LazyAttribute(
        lambda o: faker.pyint(min_value=1, max_value=31)
    )

    class Meta:
        model = CreditCard


class DebitCardFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    nickname = factory.LazyAttribute(lambda o: faker.name())
    bank = factory.SubFactory(BankMasterFactory)
    description = factory.LazyAttribute(lambda o: faker.text())
    account = factory.SubFactory(BankAccountFactory)
    vendor = factory.LazyAttribute(lambda o: random.choices(["V", "M", "MC"]))

    class Meta:
        model = DebitCard
