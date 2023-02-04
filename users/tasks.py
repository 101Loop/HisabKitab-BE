from django.conf import settings
from drfaddons.utils import send_message
from huey.contrib import djhuey as huey


@huey.task(retries=2, retry_delay=10)
def send_welcome_email_async(recip_email: str):
    """Send email async."""
    send_message(settings.WELCOME_EMAIL_BODY, settings.WELCOME_EMAIL_SUBJECT, [recip_email], [recip_email])
