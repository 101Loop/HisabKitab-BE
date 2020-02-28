from rest_framework.serializers import ModelSerializer


class SettingsSerializer(ModelSerializer):
    class Meta:
        from .models import UserSettings

        model = UserSettings
        fields = ("is_beta", "advance_mode")
        read_only_fields = ("create_date", "update_date")
