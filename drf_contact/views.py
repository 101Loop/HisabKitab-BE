from django_filters.rest_framework import DjangoFilterBackend
from drfaddons.filters import IsOwnerFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from drf_contact.models import ContactDetail
from drf_contact.serializers import (
    ShowContactDetailSerializer,
    AddContactDetailSerializer,
)


class ShowContacts(ListAPIView):
    """
    This view is to show the details of a contact.
    """

    queryset = ContactDetail.objects.all().order_by("-create_date")
    serializer_class = ShowContactDetailSerializer
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend, SearchFilter)
    search_fields = ("^name",)
    pagination_class = PageNumberPagination
    page_size = 10
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)


class AddContacts(CreateAPIView):
    """
    This view is to add new contacts.
    """

    serializer_class = AddContactDetailSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
