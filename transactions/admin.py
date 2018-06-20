from django.contrib import admin
from .models import TransactionModes, TransactionDetails


admin.site.register(TransactionModes)
admin.site.register(TransactionDetails)
