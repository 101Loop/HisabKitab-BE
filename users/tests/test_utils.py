"""Tests for drf_user/utils.py module"""
import datetime
from unittest.mock import ANY, MagicMock, patch

from django.test import TestCase
from django.utils import timezone
from rest_framework import status

from users.factories import OTPValidationFactory, UserFactory
from users.models import OTPValidation
from users.utils import (
    check_unique,
    check_validation,
    generate_otp,
    send_otp,
    validate_otp,
)


class TestCheckUnique(TestCase):
    """check_unique test"""

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = UserFactory(email="user@email.com")

    def test_check_non_unique(self):
        """Check if the user is non-unique"""
        self.assertTrue(check_unique("email", "user1@email.com"))

    def test_check_unique(self):
        """Check if the user is unique"""
        self.assertFalse(check_unique("email", "user@email.com"))


class TestCheckValidation(TestCase):
    """check_validation test"""

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.validated_otp_validation = OTPValidationFactory(
            destination="user@email.com", is_validated=True
        )

    def test_check_validated_object(self):
        """Check if the value is validated"""
        self.assertTrue(check_validation("user@email.com"))

    def test_check_non_validated_object(self):
        """Check if the value is not validated"""
        self.assertFalse(check_validation("user1@email.com"))


class TestGenerateOTP(TestCase):
    """generate_otp Test"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.opt_validation = OTPValidationFactory(
            destination="test@example.com", otp=1234567, is_validated=False
        )

    def test_generate_otp(self):
        """Check generate_otp successfully generates OTPValidation object or not"""
        generate_otp("email", "user1@email.com")
        self.assertEqual(OTPValidation.objects.count(), 2)

    def test_generate_otp_reactive_past(self):
        """
        Check generate_otp generates a new otp if the reactive time is yet to be over
        """
        otp_validation1 = generate_otp("email", "user1@email.com")
        otp_validation2 = generate_otp("email", "user1@email.com")
        self.assertNotEqual(otp_validation1.otp, otp_validation2.otp)

    def test_generate_otp_reactive_future(self):
        """
        Check generate_otp returns the same otp if the reactive time is already over
        """
        otp_validation1 = generate_otp("email", "user1@email.com")

        """
        Simulating that the reactive time is already been over 5 minutes ago
        """
        otp_validation1.reactive_at = timezone.now() + datetime.timedelta(minutes=5)
        otp_validation1.save()

        otp_validation2 = generate_otp("email", "user1@email.com")
        self.assertEqual(otp_validation2.otp, otp_validation1.otp)

    @patch("users.utils.get_random_string", return_value="1234567")
    def test_generate_otp_generates_new_otp_if_one_already_exists(
        self, mock_get_random_string: MagicMock
    ):
        """
        Check generate_otp generates a new otp if the one already exists
        """
        generate_otp("email", "test@django.com")
        self.assertEqual(OTPValidation.objects.count(), 2)
        mock_get_random_string.assert_called_once()


class TestValidateOTP(TestCase):
    """validate_otp test"""

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.otp_validation = OTPValidationFactory(
            destination="user@email.com", otp=12345
        )

    def test_validate_otp(self):
        """Check if OTPValidation object is created or not"""
        self.assertTrue(validate_otp("user@email.com", 12345))

    def test_validate_otp_returns_401_and_attempt_exceeded_message(self):
        """
        Set the validate_attempt to 0
        """
        self.otp_validation.validate_attempt = 0
        self.otp_validation.save()

        data, status_code = validate_otp("user@email.com", 56123)
        self.assertFalse(data["success"])
        self.assertEqual(data["OTP"], "Attempt exceeded! OTP has been reset!")
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_validate_otp_returns_401_and_validation_failed_message(self):
        """Check function raises attempt exceeded exception"""
        data, status_code = validate_otp("user@email.com", 5623)
        self.assertFalse(data["success"])
        self.assertEqual(data["OTP"], "OTP Validation failed! 2 attempts left!")
        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    def test_validate_otp_returns_404_for_not_existing_value(self):
        """Check function raises attempt exceeded exception"""
        value = "temp@django.com"
        data, status_code = validate_otp(value, 5623)
        self.assertFalse(data["success"])
        self.assertEqual(data["OTP"], f"Provided {value=} to verify not found!")
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)


class TestSendOTP(TestCase):
    """send_otp test"""

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.email = "user@email.com"
        cls.new_email = "new_user@email.com"
        reactive_at = timezone.now() + datetime.timedelta(minutes=5)
        old_reactive_at = timezone.now() - datetime.timedelta(minutes=5)
        cls.otp_validation = OTPValidationFactory(
            destination=cls.email, otp=1234567, reactive_at=reactive_at
        )
        cls.reactivated_otp_validation = OTPValidationFactory(
            destination=cls.new_email, otp=1234568, reactive_at=old_reactive_at
        )

    def test_otp_sending_not_allowed(self):
        data = send_otp("email", self.email, self.otp_validation, self.email)

        self.assertFalse(data["success"])
        self.assertEqual(
            data["message"],
            f"OTP sending not allowed until: {self.otp_validation.reactive_at.strftime('%d-%h-%Y %H:%M:%S')}",
        )

    @patch(
        "users.utils.send_message",
        return_value={"success": True, "message": "Message sent successfully!"},
    )
    def test_send_otp_send_email(self, mock_send_message: MagicMock):
        data = send_otp(
            "email", self.new_email, self.reactivated_otp_validation, self.new_email
        )

        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Message sent successfully!")
        self.reactivated_otp_validation.refresh_from_db()
        self.assertGreaterEqual(
            self.reactivated_otp_validation.reactive_at, timezone.now()
        )

        mock_send_message.assert_called_once_with(
            message=ANY,
            subject="OTP for Verification",
            recip_email=[self.new_email],
            recip=[self.new_email],
        )
