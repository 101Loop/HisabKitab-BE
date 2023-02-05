from django.contrib.auth import authenticate, get_user_model, get_user
from django.test import TestCase


User = get_user_model()


class TestMultiFieldModelBackend(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("test", "test@example.com", "test@123", "test", "1234567890")

    def test_authenticate_returns_none(self):
        self.assertIsNone(authenticate(username=None, password="test@123"))

    def test_authenticate_returns_none_with_invalid_password(self):
        self.assertIsNone(authenticate(username="test", password="test@1234"))

    def test_authenticate_with_mobile(self):
        self.assertEqual(authenticate(username="1234567890", password="test@123"), self.user)

    def test_authenticate_with_username(self):
        self.assertEqual(authenticate(username="test", password="test@123"), self.user)

    def test_authenticate_with_email(self):
        self.assertEqual(authenticate(username="test@example.com", password="test@123"), self.user)

    def test_authenticate_returns_none_when_user_does_not_exist(self):
        self.assertIsNone(authenticate(username="test1", password="test@123"))
