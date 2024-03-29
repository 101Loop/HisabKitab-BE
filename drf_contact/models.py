from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.text import gettext_lazy as _
from drfaddons.models import CreateUpdateModel
from rest_framework import serializers

User = get_user_model()


class ContactDetail(CreateUpdateModel):
    """
    A custom ContactDetails model that keeps a record of all the details of a contact.
    """

    name = models.CharField(_("Unique UserName"), max_length=254)
    email = models.EmailField(_("Email Address"), null=True)
    mobile = models.CharField(_("Mobile Number"), max_length=15, null=True)

    @property
    def user(self) -> User:
        if not (
            user := User.objects.filter(
                Q(email=self.email) | Q(mobile=self.mobile)
            ).first()
        ):
            raise serializers.ValidationError(
                "User with provided email or mobile does not exist"
            )

        return user

    def __str__(self):
        """
        Returns string representation of the name.
        """
        return self.name

    class Meta:
        unique_together = ("created_by", "name")
        verbose_name = _("Contact Detail")
        verbose_name_plural = _("Contact Details")
