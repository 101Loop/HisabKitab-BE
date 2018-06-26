from rest_framework.generics import ListAPIView, CreateAPIView
from .models import ContactDetails


class ShowContacts(ListAPIView):
    """
    This view is to show the details of a contact.
    """
    from .serializers import ShowContactDetailSerializer
    from rest_framework.filters import SearchFilter
    from django_custom_modules.serializer import IsOwnerFilterBackend
    from django_filters.rest_framework import DjangoFilterBackend

    queryset = ContactDetails.objects.all()
    serializer_class = ShowContactDetailSerializer
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend, SearchFilter)
    search_fields = ('^name',)


class AddContacts(CreateAPIView):
    """
    This view is to add new contacts.
    """
    from .serializers import AddContactDetailSerializer

    serializer_class = AddContactDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
