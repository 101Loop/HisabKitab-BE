from django.db import models
from django_custom_modules.data_model import CreateUpdateModel, _


class TransactionModes(CreateUpdateModel):
    """
    A custom TransactionModes model that keeps a record of all the modes of transaction.
    """

    mode = models.CharField(_('Mode of Transfer'), max_length=254, unique=True)

    def __str__(self):
        return self.mode


class TransactionDetails(CreateUpdateModel):
    """
    A custom TransactionDetails model that keeps a record of all the transaction details.
    """

    from contacts.models import ContactDetails

    contact = models.ForeignKey(ContactDetails, on_delete=models.PROTECT)
    category = models.CharField(choices=[('C', 'Credit'), ('D', 'Debit')], max_length=8)
    # TODO: Put a verification method i.e. Credit: amount >=0 | Debit: amount <=0
    amount = models.IntegerField(null=False, blank=False)
    mode = models.ForeignKey(TransactionModes, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.amount) + '|' + str(self.created_by.name)

    # def verify(self):
    #     if self.amount >= 0:
    #         self.category = 'Credit'
    #
    #     else:
    #         self.category = 'Debit'
