from django.contrib import admin

from .models import BankAccount
from .models import BankMaster
from .models import CreditCard
from .models import DebitCard


admin.site.register(BankAccount)
admin.site.register(BankMaster)
admin.site.register(CreditCard)
admin.site.register(DebitCard)
