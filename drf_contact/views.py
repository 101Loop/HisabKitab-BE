from django_filters.rest_framework import DjangoFilterBackend
from drfaddons.filters import IsOwnerFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView

from drf_contact.models import ContactDetail
from drf_contact.serializers import (
    AddContactDetailSerializer,
    ShowContactDetailSerializer,
)


class ShowContacts(ListAPIView):
    """
    This view is to show the details of a contact.
    """

    queryset = ContactDetail.objects.all().order_by("-create_date")
    serializer_class = ShowContactDetailSerializer
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend, SearchFilter)
    search_fields = ("^name",)


class AddContacts(CreateAPIView):
    """
    This view is to add new contacts.
    """

    serializer_class = AddContactDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
