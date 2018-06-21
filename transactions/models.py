from django.db import models
from django_custom_modules.data_model import CreateUpdateModel, _


class TransactionModes(CreateUpdateModel):
    mode = models.CharField(_('Mode of Transfer'), max_length=254, unique=True)


class TransactionDetails(CreateUpdateModel):
    from contacts.models import ContactDetails

    contact = models.ForeignKey(ContactDetails, on_delete=models.PROTECT)
    category = models.CharField(choices=[('+', 'Credit'), ('-', 'Debit')], max_length=8)
    # TODO: Put a verification method i.e. Credit: amount >=0 | Debit: amount <=0
    amount = models.IntegerField(default=0)
    mode = models.ForeignKey(TransactionModes, on_delete=models.PROTECT)

    # def verify(self):
    #     if self.amount >= 0:
    #         self.category = 'Credit'
    #
    #     else:
    #         self.category = 'Debit'

