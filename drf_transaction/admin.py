from django.contrib import admin

from .models import TransactionDetail, TransactionMode


class MyModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return None if obj else "created_by"


admin.site.register(TransactionMode)
admin.site.register(TransactionDetail)
