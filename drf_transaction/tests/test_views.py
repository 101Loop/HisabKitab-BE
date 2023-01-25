from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_transaction.factories import TransactionDetailFactory, TransactionModeFactory
from users.factories import UserFactory


class TestShowTransactionAmount(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("drf_transaction:show_transaction_amount")
        cls.user = UserFactory(username="temp_user")
        cls.transaction_1 = TransactionDetailFactory(created_by=cls.user)
        cls.transaction_2 = TransactionDetailFactory(created_by=cls.user)
        cls.transaction_3 = TransactionDetailFactory(created_by=cls.user)

    def test_api_raises_403_for_unauthenticated_user(self):
        """
        GIVEN: An unauthenticated user
        WHEN: The user tries to access the API
        THEN: The user should be denied access
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_raises_200_for_authenticated_user(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API
        THEN: The user should be allowed access
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_returns_all_transactions_for_authenticated_user(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API
        THEN: The user should be allowed access
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_json = response.json()
        self.assertEqual(res_json["count"], 3)
        self.assertEqual(len(res_json["results"]), 3)
        self.assertEqual(res_json["results"][0]["id"], self.transaction_3.id)
        self.assertEqual(res_json["results"][1]["id"], self.transaction_2.id)
        self.assertEqual(res_json["results"][2]["id"], self.transaction_1.id)

    def test_api_query_count(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API
        THEN: The user should be allowed access
        """
        self.client.force_authenticate(user=self.user)
        with self.assertNumQueries(3):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAddTransactionAmount(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("drf_transaction:add_transaction_amount")
        cls.user = UserFactory(username="temp_user")
        cls.mode = TransactionModeFactory(created_by=cls.user, mode="Cash")

    def test_api_raises_403_for_unauthenticated_user(self):
        """
        GIVEN: An unauthenticated user
        WHEN: The user tries to access the API
        THEN: The user should be denied access
        """
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_raises_400_for_invalid_data(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API with invalid data
        THEN: The user should be denied access
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_returns_201_for_valid_data(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API with valid data
        THEN: The user should be allowed access
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "contact": "Paid for food",
            "category": "D",
            "transaction_date": "2021-01-01",
            "amount": 1000,
            "mode": self.mode.id,
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        res_json = response.json()
        self.assertEqual(res_json["contact"], "Paid for food")
        self.assertEqual(res_json["category"], "D")
        self.assertEqual(res_json["transaction_date"], "2021-01-01")
        self.assertEqual(res_json["amount"], 1000)
        self.assertEqual(res_json["mode"], self.mode.id)
        self.assertIsNone(res_json["comments"])

    def test_api_query_count(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API with valid data
        THEN: The user should be allowed access
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "contact": "Received from friend",
            "category": "C",
            "transaction_date": "2021-01-01",
            "amount": 500,
            "mode": self.mode.id,
            "comments": "Dummy comments",
        }
        with self.assertNumQueries(6):
            response = self.client.post(self.url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        res_json = response.json()
        self.assertEqual(res_json["contact"], "Received from friend")
        self.assertEqual(res_json["comments"], "Dummy comments")
