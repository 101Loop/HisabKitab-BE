from django.db import models
from drfaddons.datatypes import UnixTimestampField
from django.utils.text import gettext_lazy as _


class Feedback(models.Model):
    """
    A Feedback model for recording the user feedback.
    """

    message = models.CharField(_('message'), max_length=200, blank=False)
    name = models.CharField(_('Unique UserName'), max_length=254)
    email = models.EmailField(_('Email Address'))
    mobile = models.CharField(_('Mobile Number'), max_length=15, null=True)
    create_date = UnixTimestampField(_('Create Date'), auto_now_add=True)

    def __str__(self):
        return 'Feedback -- ' + str(self.name)

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')

