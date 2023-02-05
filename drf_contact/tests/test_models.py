from django.test import TestCase
from rest_framework import serializers

from drf_contact.factories import ContactDetailFactory
from users.factories import UserFactory


class TestContactDetail(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory()
        cls.contact = ContactDetailFactory(
            name="John Doe", email="temp@example.com", mobile="1234567890"
        )
        cls.contact_with_user_email_and_mobile = ContactDetailFactory(
            name="Doe", email=cls.user.email, mobile=cls.user.mobile
        )

    def test_str_method(self):
        self.assertEqual(str(self.contact), "John Doe")

    def test_user_property_raises_error_if_no_user_exists_for_email_or_mobile(self):
        with self.assertRaisesMessage(
            serializers.ValidationError,
            "User with provided email or mobile does not exist",
        ):
            _ = self.contact.user

    def test_user_property_returns_user_if_user_exists_for_email_or_mobile(self):
        self.assertEqual(self.contact_with_user_email_and_mobile.user, self.user)
