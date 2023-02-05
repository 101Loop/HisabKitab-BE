from django.contrib import admin

from .models import ContactDetail


@admin.register(ContactDetail)
class ContactDetailAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "mobile"]
    readonly_fields = ["created_by", "create_date", "update_date"]
