from django.urls import reverse
from rest_framework.test import APITestCase

from users.factories import UserFactory


class TestAddContacts(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("drf_contact:add_contact")
        cls.user = UserFactory()

    def test_api_raises_403_if_not_authenticated(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_api_raises_400_if_no_data_is_passed(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_api_raises_400_if_no_name_is_passed(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.url, {"email": "temp@example.com"}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_api_creates_contact(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.url,
            {
                "name": "John Doe",
                "email": "doe@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        res_json = response.json()
        self.assertEqual(res_json["name"], "John Doe")
        self.assertEqual(res_json["email"], "doe@example.com")
