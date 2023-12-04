from django.contrib import admin

from .models import *


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ("password",)


admin.site.register(OTPValidation)
admin.site.register(AuthTransaction)
