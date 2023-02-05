from django.test import TestCase

from users.factories import AuthTransactionFactory, OTPValidationFactory, UserFactory


class TestUser(TestCase):
    """User Model"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory(name="test_user", username="my_unique_username")

    def test_get_full_name(self):
        """Checks that User.get_full_name() method returns exact name"""
        self.assertEqual(self.user.get_full_name(), "test_user")

    def test_get_short_name(self):
        """Checks that User.get_short_name() method returns exact name"""
        self.assertEqual(self.user.get_short_name(), "test_user")

    def test_str_method(self):
        """Check str method"""
        self.assertEqual(str(self.user), "test_user | my_unique_username")

    def test_is_staff(self):
        """Check is_staff method"""
        self.assertFalse(self.user.is_staff)


class TestAuthTransaction(TestCase):
    """AuthTransaction Model"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory(name="test_user", username="my_unique_username")
        cls.auth_transaction = AuthTransactionFactory(user=cls.user)

    def test_str_method(self):
        """Check str method"""
        self.assertEqual(str(self.auth_transaction), "test_user | my_unique_username")


class TestOTPValidation(TestCase):
    """OTPValidation"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.otp_validation = OTPValidationFactory(destination="temp@example.com")

    def test_str_method(self):
        """Check str method"""
        self.assertEqual(str(self.otp_validation), "temp@example.com")
