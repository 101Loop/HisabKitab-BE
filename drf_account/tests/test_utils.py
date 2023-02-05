from django.test import TestCase

from drf_account.factories import BankMasterFactory
from drf_account.utils import get_bank_by_name


class TestGetBankByName(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.axis_bank = BankMasterFactory(
            name="Axis Bank",
            aliases='[{"name": "Axis Bank", "aliases": ["Axis", "Axis Bank"] }]',
        )
        cls.central_bank = BankMasterFactory(
            name="Central Bank",
            aliases='[{"name": "Central Bank", "aliases": ["Central", "Central Bank"] }]',
        )

    def test_get_axis_bank(self):
        self.assertEqual(get_bank_by_name("Axis Bank"), self.axis_bank)

    def test_get_central_bank(self):
        self.assertEqual(get_bank_by_name("Central Bank"), self.central_bank)

    def test_get_bank_by_alias(self):
        self.assertEqual(get_bank_by_name("Central"), self.central_bank)

    def test_get_bank_by_alias_2(self):
        self.assertEqual(get_bank_by_name("Axis"), self.axis_bank)

    def test_get_bank_by_name_not_found(self):
        self.assertIsNone(get_bank_by_name("HDFC Bank"))
