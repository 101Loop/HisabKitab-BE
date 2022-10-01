from rest_framework.generics import CreateAPIView

from fcm_notification.serializers import FCMTokenSerializer


class FCMTokenApi(CreateAPIView):
    serializer_class = FCMTokenSerializer

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)
