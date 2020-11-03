from django.contrib import admin

from .models import TransactionDetail
from .models import TransactionMode


class MyModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return None
        return "created_by"


admin.site.register(TransactionMode)
admin.site.register(TransactionDetail)
