from rest_framework.generics import ListAPIView, CreateAPIView
from .models import ContactDetails
from .serializers import ShowContactDetailSerializer


class ShowContacts(ListAPIView):
    """
    This view is to show the details of a contact.
    """
    from .serializers import ShowContactDetailSerializer

    queryset = ContactDetails.objects.all()
    serializer_class = ShowContactDetailSerializer


class AddContacts(CreateAPIView):
    """
    This view is to add new contacts.
    """
    from .serializers import AddContactDetailSerializer

    serializer_class = AddContactDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
#
#     def post(self, request):
#
#         from .serializers import AddContactDetailSerializer
#         from django.http import JsonResponse
#
#         serializer = AddContactDetailSerializer(data = self.request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors)
