from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import TestCase

from users.tasks import send_welcome_email_async


class TestTasks(TestCase):
    @patch("users.tasks.send_message")
    def test_send_welcome_email_async(self, mock_send_message: MagicMock):
        email = "random@email.com"
        send_welcome_email_async(email)

        mock_send_message.assert_called_once_with(
            settings.WELCOME_EMAIL_BODY,
            settings.WELCOME_EMAIL_SUBJECT,
            [email],
            [email],
        )
