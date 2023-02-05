from django.urls import reverse
from rest_framework.test import APITestCase

from drf_account.factories import BankMasterFactory, BankAccountFactory, DebitCardFactory
from drf_account.models import BankMaster, DebitCard
from users.factories import UserFactory


class TestAddBankAccountView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("drf_account:add_bank_account")
        cls.user = UserFactory()
        cls.bank_master = BankMasterFactory(name="HDFC Bank")

    def test_api_raises_403_if_not_authenticated(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_api_raises_400_if_no_data_is_passed(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_api_raises_400_if_no_bank_name_is_passed(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {"nickname": "axis"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_api_creates_bank_and_bank_account(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.url,
            {"nickname": "axis", "bank": "Axis Bank", "description": "This is a bank", "accnumber": 88223344},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        res_json = response.json()
        self.assertEqual(res_json["nickname"], "axis")
        self.assertEqual(res_json["bank"], "Axis Bank")
        self.assertEqual(res_json["description"], "This is a bank")
        self.assertEqual(res_json["accnumber"], "88223344")

    def test_api_uses_existing_bank_to_create_account(self):
        self.client.force_authenticate(self.user)

        # check if bank exists
        self.assertEqual(BankMaster.objects.count(), 1)

        response = self.client.post(
            self.url,
            {
                "nickname": "hdfc",
                "bank": "HDFC Bank",
                "description": "My new account in another bank",
                "accnumber": 882233440,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        res_json = response.json()
        self.assertEqual(res_json["nickname"], "hdfc")
        self.assertEqual(res_json["bank"], "HDFC Bank")
        self.assertEqual(res_json["description"], "My new account in another bank")
        self.assertEqual(res_json["accnumber"], "882233440")

        # check only one bank exists
        self.assertEqual(BankMaster.objects.count(), 1)


class TestAddDebitCardView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("drf_account:add_debit_card")
        cls.user = UserFactory()
        cls.bank_master = BankMasterFactory(name="HDFC Bank")
        cls.bank_account = BankAccountFactory(bank=cls.bank_master)

    def test_api_raises_403_if_not_authenticated(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_api_raises_400_if_no_data_is_passed(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_api_raises_400_if_no_bank_name_is_passed(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {"nickname": "axis"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_api_raises_400_if_both_bank_and_account_are_not_passed(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {"nickname": "axis", "vendor": "MC"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_api_creates_bank_and_debit_card(self):
        self.client.force_authenticate(self.user)

        # assert debit card does not exist
        self.assertEqual(DebitCard.objects.count(), 0)

        response = self.client.post(
            self.url,
            {
                "nickname": "axis",
                "bank": "Axis Bank",
                "description": "This is a bank",
                "vendor": "V",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        res_json = response.json()
        self.assertEqual(res_json["nickname"], "axis")
        self.assertEqual(res_json["bank"], "Axis Bank")
        self.assertEqual(res_json["description"], "This is a bank")
        self.assertEqual(res_json["vendor"], "V")

        # assert debit card exists
        self.assertEqual(DebitCard.objects.count(), 1)
        self.assertEqual(BankMaster.objects.count(), 2)

    def test_api_uses_bank_from_account(self):
        self.client.force_authenticate(self.user)

        # assert debit card does not exist
        self.assertEqual(DebitCard.objects.count(), 0)

        response = self.client.post(
            self.url,
            {
                "nickname": "new dc",
                "vendor": "MC",
                "account": self.bank_account.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        res_json = response.json()
        self.assertEqual(res_json["bank"], "HDFC Bank")
        self.assertEqual(res_json["vendor"], "MC")

        # assert debit card exists
        self.assertEqual(DebitCard.objects.count(), 1)
        self.assertEqual(BankMaster.objects.count(), 1)


class TestShowDebitCardView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("drf_account:show_debit_card")
        cls.user = UserFactory()
        cls.bank_master_1 = BankMasterFactory(name="HDFC Bank")
        cls.bank_master_2 = BankMasterFactory(name="Axis Bank")
        cls.bank_account_1 = BankAccountFactory(bank=cls.bank_master_1)
        cls.bank_account_2 = BankAccountFactory(bank=cls.bank_master_2)
        cls.debit_card_1 = DebitCardFactory(account=cls.bank_account_1, bank=cls.bank_master_1, created_by=cls.user)
        cls.debit_card_2 = DebitCardFactory(account=cls.bank_account_2, bank=cls.bank_master_2, created_by=cls.user)

    def test_api_raises_403_if_not_authenticated(self):
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_api_returns_debit_card(self):
        # TODO: Ideally we should filter by created_by on this endpoint
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        res_json = response.json()
        self.assertEqual(res_json["count"], 2)
        self.assertEqual(res_json["next"], None)
        self.assertEqual(res_json["previous"], None)
        self.assertEqual(len(res_json["results"]), 2)
