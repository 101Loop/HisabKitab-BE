from rest_framework import serializers


class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:

        from .models import FCMToken

        model = FCMToken
        fields = ("token",)
