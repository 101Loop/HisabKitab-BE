from django.contrib import admin

from .models import BankAccount, BankMaster, CreditCard, DebitCard

admin.site.register(BankAccount)
admin.site.register(BankMaster)
admin.site.register(CreditCard)
admin.site.register(DebitCard)
