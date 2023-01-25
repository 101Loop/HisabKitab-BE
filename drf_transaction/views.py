from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from drfaddons.filters import IsOwnerFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_contact.models import ContactDetail
from drf_transaction.filters import RangeFiltering
from drf_transaction.models import TransactionDetail, TransactionMode
from drf_transaction.serializers import (
    AddTransactionDetailsSerializer,
    ShowTransactionDetailsSerializer,
    UpdateTransactionDetailsSerializer,
    ShowModeSerializer,
    DeleteTransactionDetailsSerializer,
)


class ShowTransactionAmount(ListAPIView):
    """
    This view is to show the details of transactions.
    """

    queryset = (
        TransactionDetail.objects.select_related("contact", "mode")
        .all()
        .order_by("-transaction_date")
        .order_by("-create_date")
    )
    serializer_class = ShowTransactionDetailsSerializer
    filter_backends = (
        IsOwnerFilterBackend,
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filter_class = RangeFiltering
    search_fields = ("^contact__name",)
    ordering_fields = ("contact__name", "amount", "transaction_date")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total = queryset.aggregate(Sum("amount"))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.data["total_amount"] = total["amount__sum"]
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AddTransactionAmount(CreateAPIView):
    """
    This view is to add new transactions.
    """

    serializer_class = AddTransactionDetailsSerializer
    parser_classes = (JSONParser,)

    def perform_create(self, serializer):
        contact_obj, _ = ContactDetail.objects.get_or_create(
            name=serializer.validated_data["contact"], created_by=self.request.user
        )
        serializer.validated_data["contact"] = contact_obj
        serializer.save(created_by=self.request.user)


class DeleteTransactionAmount(DestroyAPIView):
    """
    This view is to delete a transaction.
    """

    filter_backends = (IsOwnerFilterBackend,)
    queryset = TransactionDetail.objects.all()
    serializer_class = DeleteTransactionDetailsSerializer


class UpdateTransactionAmount(UpdateAPIView):
    """
    This view is to update a transaction.
    """

    queryset = TransactionDetail.objects.all()
    serializer_class = UpdateTransactionDetailsSerializer
    filter_backends = (IsOwnerFilterBackend,)

    def perform_update(self, serializer):
        if "contact" in serializer.initial_data.keys():
            contact_obj, _ = ContactDetail.objects.get_or_create(
                name=serializer.validated_data["contact"], created_by=self.request.user
            )
            serializer.validated_data["contact"] = contact_obj

        serializer.save(created_by=self.request.user)


class ShowMode(ListAPIView):
    """
    This view will show all the modes of transaction.
    """

    permission_classes = (AllowAny,)
    queryset = TransactionMode.objects.all().order_by("-create_date")
    serializer_class = ShowModeSerializer
    filter_backends = ()
