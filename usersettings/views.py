from rest_framework.generics import RetrieveUpdateAPIView


class ChangeSettingsView(RetrieveUpdateAPIView):
    """
    This view is to check the type of user.
    """
    from .serializers import SettingsSerializer

    serializer_class = SettingsSerializer

    def get_object(self):
        from .models import UserSettings

        try:
            obj = UserSettings.objects.get(pk=self.request.user)
        except UserSettings.DoesNotExist:
            obj = UserSettings()
            obj.created_by = self.request.user
            obj.save()
        return obj
