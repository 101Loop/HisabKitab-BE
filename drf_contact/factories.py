import factory
from django.contrib.auth import get_user_model
from faker import Faker

from drf_contact.models import ContactDetail
from users.factories import UserFactory

User = get_user_model()

faker = Faker()


class ContactDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactDetail

    name = factory.LazyAttribute(lambda o: faker.name())
    email = factory.LazyAttribute(lambda o: faker.email())
    mobile = factory.LazyAttribute(lambda o: faker.phone_number())
    created_by = factory.SubFactory(UserFactory)
