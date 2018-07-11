from django.db import models
from drfaddons.models import CreateUpdateModel
from django.utils.text import gettext_lazy as _


class TransactionModes(CreateUpdateModel):
    """
    A custom TransactionModes model that keeps a record of all the modes of transaction.
    """

    mode = models.CharField(_('Mode of Transfer'), max_length=254, unique=True)

    def __str__(self):
        return self.mode

    class Meta:
        verbose_name = _('Transaction Mode')
        verbose_name_plural = _('Transaction Modes')


class TransactionDetails(CreateUpdateModel):
    """
    A custom TransactionDetails model that keeps a record of all the transaction details.
    """

    from contacts.models import ContactDetails

    contact = models.ForeignKey(ContactDetails, on_delete=models.PROTECT)
    category = models.CharField(_('Category'), choices=[('C', 'Credit'), ('D', 'Debit')], max_length=6)
    transaction_date = models.DateField(_('Transaction Date'))
    amount = models.FloatField(_('Amount'), null=False, blank=False)
    mode = models.ForeignKey(TransactionModes, on_delete=models.PROTECT)
    comments = models.TextField(_('Comments'), null=True, blank=True)

    def __str__(self):
        return str(self.amount) + '|' + str(self.created_by.name)

    class Meta:
        verbose_name = _('Transaction Detail')
        verbose_name_plural = _('Transaction Details')
