from django.test import TestCase

from drf_transaction.factories import TransactionModeFactory, TransactionDetailFactory


class TestTransactionMode(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.transaction_mode = TransactionModeFactory(mode="cash")

    def test_str_method(self):
        self.assertEqual(str(self.transaction_mode), "cash")


class TransactionDetail(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.transaction_detail = TransactionDetailFactory()

    def test_str_method(self):
        self.assertEqual(
            str(self.transaction_detail),
            f"{str(self.transaction_detail.amount)}|{str(self.transaction_detail.created_by.name)}",
        )
