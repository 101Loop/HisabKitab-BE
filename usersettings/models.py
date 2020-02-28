from django.db import models
from drfaddons.models import CreateUpdateModel
from django.utils.text import gettext_lazy as _


class UserSettings(CreateUpdateModel):
    """
    A custom UserSettings model that keeps a record of the type of mode of the user.
    """

    from django.contrib.auth import get_user_model

    advance_mode = models.BooleanField(_("Advance Mode"), default=False)
    is_beta = models.BooleanField(_("Is Beta User"), default=False)
    created_by = models.OneToOneField(
        get_user_model(), primary_key=True, on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "User Setting"
        verbose_name_plural = "User Settings"
