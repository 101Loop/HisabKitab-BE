from django.contrib import admin


class MyModelAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return None
        return 'created_by'
