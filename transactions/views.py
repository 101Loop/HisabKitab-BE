from .models import TransactionDetails
from rest_framework.generics import ListAPIView, CreateAPIView


class ShowTransactionAmount(ListAPIView):
    """
    This view is to show the details of transactions.
    """
    from .serializers import ShowTransactionDetailsSerializer


    queryset = TransactionDetails.objects.all()
    serializer_class = ShowTransactionDetailsSerializer
    # TODO: Check how to send range
    # TODO: Check how to send multiple value (cash & cheque)
    # TODO: Fix pagination error: Define Ordering parameter
    # TODO: Implement ordering (Sorting)
    filter_fields = ('category', 'mode')


class AddTransactionAmount(CreateAPIView):
    """
    This view is to add new transactions.
    """
    from .serializers import AddTransactionDetailsSerializer

    serializer_class = AddTransactionDetailsSerializer

    def perform_create(self, serializer):

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
