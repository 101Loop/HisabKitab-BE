from rest_framework import serializers

from fcm_notification.models import FCMToken


class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMToken
        fields = ("token",)
