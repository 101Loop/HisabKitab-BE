from django.db import models
from django_custom_modules.data_model import CreateUpdateModel, _


class FCMToken(CreateUpdateModel):

    token = models.CharField(_('Message'), max_length=254)

    def __str__(self):
        return self.token
