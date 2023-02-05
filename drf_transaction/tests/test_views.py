from unittest.mock import MagicMock, patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_contact.factories import ContactDetailFactory
from drf_transaction.factories import TransactionDetailFactory, TransactionModeFactory
from drf_transaction.models import TransactionDetail
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

    @patch(
        "drf_transaction.views.ShowTransactionAmount.pagination_class",
        return_value=None,
    )
    def test_response_without_pagination(self, mock_paginator: MagicMock):
        """
        GIVEN: An authenticated user
        WHEN: Pagination is disabled
        THEN: Response should not contain pagination
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_json = response.json()
        self.assertTrue(isinstance(res_json, list))
        self.assertEqual(res_json[0]["id"], self.transaction_3.id)
        self.assertEqual(res_json[1]["id"], self.transaction_2.id)
        self.assertEqual(res_json[2]["id"], self.transaction_1.id)

        mock_paginator.assert_called_once()

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


class TestDeleteTransactionAmount(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="temp_user")
        cls.transaction = TransactionDetailFactory(created_by=cls.user)
        cls.url = reverse(
            "drf_transaction:delete_transaction_amount",
            kwargs={"pk": cls.transaction.id},
        )

    def test_api_raises_403_for_unauthenticated_user(self):
        """
        GIVEN: An unauthenticated user
        WHEN: The user tries to access the API
        THEN: The user should be denied access
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_raises_404_for_invalid_pk(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API with invalid pk
        THEN: The user should be denied access
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("drf_transaction:delete_transaction_amount", kwargs={"pk": 100})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_returns_204_for_valid_pk(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API with valid pk
        THEN: Delete the transaction and return 204 status code
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TransactionDetail.objects.count(), 0)

    def test_api_query_count(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API with valid pk
        THEN: Delete the transaction and return 204 status code
        """
        self.client.force_authenticate(user=self.user)
        with self.assertNumQueries(2):
            response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestUpdateTransactionAmount(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="temp_user")
        cls.contact = ContactDetailFactory(
            created_by=cls.user, name="Received from friend"
        )
        cls.transaction = TransactionDetailFactory(
            created_by=cls.user, contact=cls.contact
        )
        cls.url = reverse(
            "drf_transaction:update_transaction_amount",
            kwargs={"pk": cls.transaction.id},
        )

    def test_api_raises_403_for_unauthenticated_user(self):
        """
        GIVEN: An unauthenticated user
        WHEN: The user tries to access the API
        THEN: The user should be denied access
        """
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_raises_404_for_invalid_pk(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API with invalid pk
        THEN: The user should be denied access
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("drf_transaction:update_transaction_amount", kwargs={"pk": 100})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_updates_amount(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API with valid pk
        THEN: Update the transaction and return 200 status code
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "amount": 1500,
        }
        with self.assertNumQueries(3):
            response = self.client.put(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_json = response.json()
        self.assertEqual(res_json["amount"], 1500)

    def test_api_updates_amount_with_same_contact(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API with valid pk
        THEN: Update the transaction and return 200 status code
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "contact": "Received from friend",
            "amount": 1200,
        }
        with self.assertNumQueries(4):
            response = self.client.put(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_json = response.json()
        self.assertEqual(res_json["contact"], "Received from friend")
        self.assertEqual(res_json["amount"], 1200)

    def test_api_updates_amount_with_new_contact(self):
        """
        GIVEN: An authenticated user
        WHEN: The user tries to access the API with valid pk
        THEN: Update the transaction and return 200 status code
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "contact": "Received from brother",
            "amount": 1200,
        }
        with self.assertNumQueries(6):
            response = self.client.put(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_json = response.json()
        self.assertEqual(res_json["contact"], "Received from brother")
        self.assertEqual(res_json["amount"], 1200)


class TestShowMode(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username="temp_user")
        cls.mode_1 = TransactionModeFactory(created_by=cls.user, mode="Cash")
        cls.mode_2 = TransactionModeFactory(created_by=cls.user, mode="Card")
        cls.mode_3 = TransactionModeFactory(created_by=cls.user, mode="UPI")
        cls.url = reverse("drf_transaction:show_mode")

    def test_api_returns_200_for_all_users(self):
        """
        GIVEN: Any user
        WHEN: The user tries to access the API
        THEN: The user should be allowed access
        """
        with self.assertNumQueries(2):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_json = response.json()
        self.assertEqual(res_json["count"], 3)
        self.assertEqual(res_json["results"][0]["mode"], "UPI")
        self.assertEqual(res_json["results"][1]["mode"], "Card")
        self.assertEqual(res_json["results"][2]["mode"], "Cash")
