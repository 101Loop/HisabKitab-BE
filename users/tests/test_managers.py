"""Tests for drf_user/managers.py module"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker

User = get_user_model()

faker: Faker = Faker()


class TestUserManager(TestCase):
    """TestUserManager

    Check that all methods in UserManager works as expected.
    """

    def test_create_normal_user_with_mobile(self):
        """Check that normal user is created with mobile number"""
        # given
        name = faker.name()
        user_name = faker.user_name()
        email = faker.email()
        password = faker.password()
        mobile = faker.phone_number()

        # when
        user = User.objects.create_user(
            username=user_name, email=email, password=password, name=name, mobile=mobile
        )

        # then
        self.assertEqual(user.name, name)
        self.assertEqual(user.username, user_name)
        self.assertEqual(user.email, email)
        self.assertIsNotNone(user.mobile)
        self.assertFalse(user.is_superuser)

    def test_create_super_user_with_mobile(self):
        """Check that superuser is created with mobile number"""
        # given
        name = faker.name()
        user_name = faker.user_name()
        email = faker.email()
        password = faker.password()
        mobile = faker.phone_number()

        # when
        user = User.objects.create_superuser(
            username=user_name, email=email, password=password, name=name, mobile=mobile
        )

        # then
        self.assertEqual(user.name, name)
        self.assertEqual(user.username, user_name)
        self.assertEqual(user.email, email)
        self.assertIsNotNone(user.mobile)
        self.assertTrue(user.is_superuser)

    def test_create_super_user_raises_value_error_when_is_super_user_false(self):
        """
        Check that create_super_user raises value error if is_superuser set to False
        """
        # given
        name = faker.name()
        user_name = faker.user_name()
        email = faker.email()
        password = faker.password()
        mobile = faker.phone_number()

        # then
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username=user_name,
                email=email,
                password=password,
                name=name,
                mobile=mobile,
                is_superuser=False,
            )

    def test_create_user_raises_value_error_when_email_is_none(self):
        """
        Check that create_super_user raises value error if email is None
        """
        # given
        name = faker.name()
        user_name = faker.user_name()
        password = faker.password()
        mobile = faker.phone_number()

        # then
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username=user_name,
                email=None,
                password=password,
                name=name,
                mobile=mobile,
            )
