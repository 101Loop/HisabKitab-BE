from .models import TransactionDetails
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response


class ShowTransactionAmount(ListAPIView):
    """
    This view is to show the details of transactions.
    """
    from .serializers import ShowTransactionDetailsSerializer
    from django_custom_modules.serializer import IsOwnerFilterBackend
    from django_filters.rest_framework import DjangoFilterBackend, MultipleChoiceFilter
    from rest_framework.filters import SearchFilter, OrderingFilter

    queryset = TransactionDetails.objects.all().order_by('contact_id')
    serializer_class = ShowTransactionDetailsSerializer
    filter_backends = (IsOwnerFilterBackend, DjangoFilterBackend, SearchFilter, OrderingFilter)
    # TODO: Check how to send range
    # TODO: Check how to send multiple value (cash & cheque)

    filter_fields = ('category', 'mode', 'id', 'transaction_date', 'amount')
    search_fields = ('^contact__name', )
    ordering_fields = ('contact__name', 'amount', 'transaction_date')

    def list(self, request, *args, **kwargs):
        from django.db.models import Sum

        queryset = self.filter_queryset(self.get_queryset())
        total = queryset.aggregate(Sum('amount'))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.data['total_amount'] = total['amount__sum']
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AddTransactionAmount(CreateAPIView):
    """
    This view is to add new transactions.
    """
    from .serializers import AddTransactionDetailsSerializer
    from rest_framework.parsers import JSONParser

    serializer_class = AddTransactionDetailsSerializer
    parser_classes = (JSONParser,)

    def perform_create(self, serializer):

        from contacts.models import ContactDetails

        contact_obj, create = ContactDetails.objects.get_or_create(name=serializer.validated_data['contact'],
                                                                    created_by=self.request.user)
        serializer.validated_data['contact'] = contact_obj
        serializer.save(created_by=self.request.user)


class DeleteTransactionAmount(DestroyAPIView):
    """
    This view is to delete a transaction.
    """
    from .serializers import DeleteTransactionDetailsSerializer

    queryset = TransactionDetails.objects.all()
    serializer_class = DeleteTransactionDetailsSerializer
    lookup_field = 'id'


class UpdateTransactionAmount(UpdateAPIView):
    """
    This view is to update a transaction.
    """
    from .serializers import UpdateTransactionDetailsSerializer

    queryset = TransactionDetails.objects.all()
    serializer_class = UpdateTransactionDetailsSerializer

    def perform_update(self, serializer):

        from contacts.models import ContactDetails

        contact_obj, created = ContactDetails.objects.get_or_create(name=serializer.validated_data['contact'],
                                                                    created_by=self.request.user)
        serializer.validated_data['contact'] = contact_obj
        serializer.save(created_by=self.request.user)


class ShowMode(ListAPIView):
    """
    This view will show all the modes of transaction.
    """
    from .serializers import ShowModeSerializer
    from .models import TransactionModes
    from rest_framework.permissions import AllowAny

    permission_classes = (AllowAny, )
    queryset = TransactionModes.objects.all()
    serializer_class = ShowModeSerializer
    filter_backends = ()


def about(request):
    """
    This function is used to set the about page.
    """
    from django.shortcuts import render

    return render(request, 'transactions/about.html')
