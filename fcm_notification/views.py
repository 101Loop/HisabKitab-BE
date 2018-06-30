from rest_framework.generics import CreateAPIView


class FCMTokenApi(CreateAPIView):

    from .serializers import FCMTokenSerializer

    serializer_class = FCMTokenSerializer

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)
