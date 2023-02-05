from django.contrib import admin

from .models import TransactionDetail, TransactionMode

admin.site.register(TransactionMode)
admin.site.register(TransactionDetail)
