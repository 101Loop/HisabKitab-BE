from unittest import mock
from unittest.mock import MagicMock, patch

import fakeredis
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.factories import UserFactory
from users.models import User


class TestLoginAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("users:login")

    def test_login_with_invalid_creds(self):
        data = {"username": "test", "password": "test"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["data"]["token"])
        self.assertIsNotNone(response.json()["data"]["session"])


class TestRegisterAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("users:register")
        cls.user = UserFactory(username="random", email="random@email.com", mobile="8800880088")

    @mock.patch("users.views.send_welcome_email_async")
    @mock.patch("users.views.get_redis_conn", return_value=fakeredis.FakeStrictRedis())
    def test_register(self, mock_redis: MagicMock, mock_send_welcome_email_async: MagicMock):
        data = {
            "username": "test",
            "password": "test",
            "email": "test@example.com",
            "mobile": "1234567890",
            "name": "test",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()["data"]
        self.assertEqual(data["username"], "test")
        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["mobile"], "1234567890")
        self.assertEqual(data["name"], "test")
        mock_send_welcome_email_async.assert_called()
        mock_redis.assert_called()


class TestCheckUniqueAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("users:check_unique")
        cls.user = UserFactory(username="random")

    def test_check_unique_returns_false_for_existing_username(self):
        data = {"prop": "username", "value": "random"}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertFalse(json["data"]["unique"])

    def test_check_unique_returns_true_for_non_existing_username(self):
        data = {"prop": "username", "value": "random1"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertTrue(json["data"]["unique"])


class TestLoginOTPAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("users:login_otp")
        cls.email = "random@test.com"
        cls.user = UserFactory(email=cls.email)

    def test_user_does_not_exists(self):
        data = {"value": "random@example.com"}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json = response.json()
        self.assertFalse(json["data"]["success"])
        self.assertEqual(json["data"]["message"], "No user exists with provided details!")

    @patch("users.utils.send_message", return_value={"success": True, "message": "Message sent successfully!"})
    def test_user_exists_with_null_otp(self, mock_send_message: MagicMock):
        data = {"value": self.email}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        json = response.json()
        self.assertTrue(json["data"]["success"])
        self.assertEqual(json["data"]["message"], "Message sent successfully!")
        mock_send_message.assert_called_once()

    @patch("users.views.validate_otp", return_value=({}, status.HTTP_202_ACCEPTED))
    def test_login_user_with_valid_otp(self, mock_validate_otp: MagicMock):
        data = {"value": self.email, "otp": "12345"}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertIn("token", json["data"])
        self.assertIn("session", json["data"])

        mock_validate_otp.assert_called_once()


class TestChangePasswordAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("users:change_password")
        cls.user = UserFactory()

    def test_api_raises_403_for_unauthenticated_user(self):
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_raises_400_for_empty_data(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_updates_password(self):
        self.client.force_authenticate(self.user)
        data = {"new_password": "test1"}
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("test1"))


class TestUpdateProfileViewAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("users:update_profile")
        cls.email = "random@email.com"
        cls.user = UserFactory(email=cls.email)
        cls.new_user = UserFactory(email="random1@email.com")

    def test_api_raises_403_for_unauthenticated_user(self):
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_raises_400_for_empty_data(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["data"]["non_field_errors"], ['Please provide at least one field to update.'])

    def test_api_raises_400_if_user_exists_for_given_data(self):
        self.client.force_authenticate(self.user)
        data = {"email": "random1@email.com"}
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), ['Given mobile number or email is already registered.'])

    def test_api_updates_profile_attributes(self):
        self.client.force_authenticate(self.user)
        data = {"email": "new@email.com"}
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, data["email"])


class TestUserProfileViewAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("users:user_profile")
        cls.user = UserFactory()


    def test_api_raises_403_for_unauthenticated_user(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_returns_user_profile(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()[0]
        self.assertEqual(json["name"], self.user.name)
        self.assertEqual(json["email"], self.user.email)
        self.assertEqual(json["mobile"], self.user.mobile)