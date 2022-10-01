from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import gettext_lazy as _
from drfaddons.models import CreateUpdateModel


class ContactDetail(CreateUpdateModel):
    """
    A custom ContactDetails model that keeps a record of all the details of a contact.
    """

    name = models.CharField(_("Unique UserName"), max_length=254)
    email = models.EmailField(_("Email Address"), null=True)
    mobile = models.CharField(_("Mobile Number"), max_length=15, null=True)

    @property
    def user(self):

        usr = get_user_model()

        try:
            email_user = usr.objects.get(email=self.email)
        except usr.DoesNotExist:
            email_user = None

        try:
            mobile_user = usr.objects.get(mobile=self.mobile)
        except usr.DoesNotExist:
            mobile_user = None

        # TODO: Handle following situation in better way.
        if (
            (email_user or mobile_user)
            and mobile_user
            and email_user
            and email_user == mobile_user
            or not email_user
            and not mobile_user
            or not mobile_user
            or not email_user
        ):
            # This is ideal case
            return email_user or mobile_user
        else:
            # TODO: How two users can exist where in the contact is same?
            return email_user

    def __str__(self):
        """
        Returns string representation of the name.
        """
        return self.name

    class Meta:

        unique_together = ("created_by", "name")
        verbose_name = _("Contact Detail")
        verbose_name_plural = _("Contact Details")
