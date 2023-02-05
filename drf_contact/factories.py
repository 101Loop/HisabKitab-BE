import factory
from faker import Faker

from drf_contact.models import ContactDetail
from users.factories import UserFactory

faker = Faker()


class ContactDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactDetail

    name = factory.LazyAttribute(lambda o: faker.name())
    email = factory.LazyAttribute(lambda o: faker.email())
    mobile = factory.LazyAttribute(lambda o: faker.phone_number())
    created_by = factory.SubFactory(UserFactory)
