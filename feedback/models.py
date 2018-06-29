from django.db import models
from django_custom_modules.db_type import UnixTimestampField
from django.utils.text import gettext_lazy as _

class Feedback(models.Model):

    message = models.CharField(_('message'), max_length=200, blank=False)
    name = models.CharField(_('Unique UserName'), max_length=254)
    email= models.EmailField(_('Email Address'), null=True)
    mobile = models.CharField(_('Mobile Number'), max_length=15, null=True)
    create_date = UnixTimestampField(_('Create Date'), auto_now_add=True)
