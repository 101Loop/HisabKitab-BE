from unittest import mock
from unittest.mock import MagicMock

from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import User


class TestLoginAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("users:Login")

    def test_login_with_invalid_creds(self):
        data = {"username": "test", "password": "test"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()["data"],
            {"non_field_errors": ["Unable to log in with provided credentials."]},
        )

    def test_login_with_valid_creds(self):
        User.objects.create_user(
            username="test",
            password="test",
            email="test@example.com",
            name="test",
            mobile="1234567890",
            is_active=True,
        )
        data = {"username": "test", "password": "test"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()["data"]["token"])
        self.assertIsNotNone(response.json()["data"]["session"])


class TestRegisterAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("users:Register")

    @mock.patch("users.views.send_welcome_email_async")
    def test_register(self, mock_send_welcome_email_async: MagicMock):
        data = {
            "username": "test",
            "password": "test",
            "email": "test@example.com",
            "mobile": "1234567890",
            "name": "test",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)
        data = response.json()["data"]
        self.assertEqual(data["username"], "test")
        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["mobile"], "1234567890")
        self.assertEqual(data["name"], "test")
        mock_send_welcome_email_async.assert_called()
