from django.db import models
from django.utils.text import gettext_lazy as _
from drfaddons.models import CreateUpdateModel


class FCMToken(CreateUpdateModel):

    token = models.CharField(_("Message"), max_length=254)

    def __str__(self):
        return self.token
