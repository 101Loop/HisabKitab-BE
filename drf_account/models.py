import json

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import gettext_lazy as _
from drfaddons.models import CreateUpdateModel


class BankMaster(CreateUpdateModel):
    """
    This is a custom BankMaster model that keeps a record of all the banks.
    """

    name = models.CharField(_("Bank Name"), max_length=254, unique=True)
    aliases = models.TextField(_("Aliases of Bank Name"), null=True, blank=False)

    @property
    def bank_aliases(self):
        return json.loads(self.aliases) if self.aliases else None

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"


class BankAccount(CreateUpdateModel):
    """
    This is a custom BankAccount model that keeps a record of all the bank details.
    """

    nickname = models.CharField(_("Nick Name"), max_length=250)
    bank = models.ForeignKey(BankMaster, on_delete=models.PROTECT)
    description = models.TextField(_("Description"), null=True)
    accnumber = models.TextField(_("Account Number"), null=True)
    minbal = models.IntegerField(_("Minimum Balance"), default=0)

    class Meta:
        unique_together = ("nickname", "created_by")
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"


class Card(CreateUpdateModel):
    """
    This is a custom Card model that keeps a record of all the Card details.
    """

    nickname = models.CharField(_("Nick Name"), max_length=250)
    bank = models.ForeignKey(BankMaster, on_delete=models.PROTECT)
    description = models.TextField(_("Description"), null=True)
    account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, null=True)
    vendor = models.CharField(
        _("Card Vendor"),
        choices=[
            ("V", "VISA"),
            ("M", "MAESTRO"),
            ("MC", "MASTER CARD"),
            ("AMX", "AMERICAN EXPRESS"),
            ("R", "RUPAY"),
        ],
        max_length=5,
    )

    def __str__(self):
        return f"{str(self.nickname)}, {self.bank.name}"

    class Meta:
        unique_together = ("nickname", "created_by")
        abstract = True


class CreditCard(Card):
    """
    This is a custom Card model that keeps a record of all the credit card details.
    It has a foreign key linking to card.
    """

    limit = models.DecimalField(_("Limit on Card"), max_digits=50, decimal_places=5)
    statement_date = models.IntegerField(
        _("Statement Generation Date"),
        validators=[MinValueValidator(1), MaxValueValidator(31)],
    )
    duedate_duration = models.IntegerField(
        _("Statement Date - Due Date Duration"), default=20
    )

    @property
    def duedate(self):
        return self.statement_date + self.duedate_duration

    class Meta:
        verbose_name = "Credit Card"
        verbose_name_plural = "Credit Cards"


class DebitCard(Card):
    """
    This is a custom Card model that keeps a record of all the debit card details.
    It has a foreign key linking to card.
    """

    free_atmtransaction = models.IntegerField(_("Free ATM Transaction"), default=10)
    free_own_atmtransaction = models.IntegerField(
        _("Free Own ATM Transaction"), default=5
    )

    @property
    def free_other_atmtransaction(self):
        return self.free_atmtransaction - self.free_own_atmtransaction

    class Meta:
        verbose_name = "Debit Card"
        verbose_name_plural = "Debit Cards"
