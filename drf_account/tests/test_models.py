from django.test import TestCase

from drf_account.factories import BankMasterFactory, CreditCardFactory, BankAccountFactory, DebitCardFactory


class TestBankMaster(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.bank_master = BankMasterFactory(
            name="Axis Bank", aliases='[{"name": "Axis Bank", "aliases": ["Axis", "Axis Bank"] }]'
        )

    def test_str(self):
        self.assertEqual(str(self.bank_master), "Axis Bank")

    def test_bank_aliases(self):
        self.assertEqual(self.bank_master.bank_aliases, [{"name": "Axis Bank", "aliases": ["Axis", "Axis Bank"]}])


class TestCreditCard(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.bank_master = BankMasterFactory(
            name="Axis Bank", aliases='[{"name": "Axis Bank", "aliases": ["Axis", "Axis Bank"] }]'
        )
        cls.account = BankAccountFactory(bank=cls.bank_master)
        cls.credit_card = CreditCardFactory(
            nickname="axis",
            bank=cls.bank_master,
            description="Axis Bank Credit Card",
            account=cls.account,
            limit=10000,
            statement_date=1,
            duedate_duration=10,
        )

    def test_str(self):
        self.assertEqual(str(self.credit_card), "axis, Axis Bank")

    def test_due_date(self):
        self.assertEqual(self.credit_card.duedate, 11)


class TestDebitCard(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.bank_master = BankMasterFactory(
            name="Axis Bank", aliases='[{"name": "Axis Bank", "aliases": ["Axis", "Axis Bank"] }]'
        )
        cls.account = BankAccountFactory(bank=cls.bank_master)
        cls.debit_card = DebitCardFactory(
            nickname="axis",
            bank=cls.bank_master,
            description="Axis Bank Debit Card",
            account=cls.account,
        )

    def test_str(self):
        self.assertEqual(str(self.debit_card), "axis, Axis Bank")

    def test_free_other_atmtransactions(self):
        self.assertEqual(self.debit_card.free_other_atmtransaction, 5)
