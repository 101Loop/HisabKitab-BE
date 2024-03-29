from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """
    A Custom USER Model. This model has ad-on properties in compare to original DJango User Mobile. This has been
    done considering the need of relevant data in real world (or Indian) scenario.
    """

    from .managers import UserManager

    username = models.CharField(_("Unique UserName"), max_length=254, unique=True)
    email = models.EmailField(_("EMail Address"), unique=True)
    mobile = models.CharField(_("Mobile Number"), max_length=150, unique=True)
    name = models.CharField(_("Full Name"), max_length=500, blank=False)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    last_modified = models.DateTimeField(_("Date Modified"), auto_now=True)
    is_active = models.BooleanField(_("Activated"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "mobile", "email"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return f"{self.name} | {self.username}"

    @property
    def is_staff(self):
        return self.is_superuser


class AuthTransaction(models.Model):
    """
    This Model keeps the record of all authentication that is taking place.
    """

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    ip_address = models.GenericIPAddressField(blank=False, null=False)
    date_created = models.DateTimeField(_("Created On"), auto_now_add=True)
    token = models.TextField(_("JWT Token passed"))
    session = models.TextField(_("Session Passed"))

    def __str__(self):
        return f"{self.user.name} | {self.user.username}"

    class Meta:
        verbose_name = _("Auth Transaction")
        verbose_name_plural = _("Auth Transactions")


class OTPValidation(models.Model):
    """
    This model keeps a record of OTP Validation and which destinations have been successfully validated.
    """

    otp = models.CharField(_("OTP Code"), max_length=10, unique=True)
    destination = models.CharField(
        _("Destination Address (Mobile/EMail)"), max_length=254, unique=True
    )
    create_date = models.DateTimeField(_("Create Date"), auto_now_add=True)
    last_modified = models.DateTimeField(_("Date Modified"), auto_now=True)
    is_validated = models.BooleanField(_("Is Validated"), default=False)
    validate_attempt = models.IntegerField(_("Attempted Validation"), default=3)
    type = models.CharField(
        _("EMail/Mobile"),
        default="email",
        max_length=15,
        choices=[("email", "EMail Address"), ("mobile", "Mobile Number")],
    )
    send_counter = models.IntegerField(_("OTP Sent Counter"), default=0)
    sms_id = models.CharField(_("SMS ID"), max_length=254, null=True, blank=True)
    reactive_at = models.DateTimeField(
        _("ReActivate Sending OTP"), default=timezone.now
    )

    def __str__(self):
        return self.destination

    class Meta:
        verbose_name = _("OTP Validation")
        verbose_name_plural = _("OTP Validations")
