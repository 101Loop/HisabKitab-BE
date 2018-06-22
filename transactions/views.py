from .models import TransactionDetails
from rest_framework.generics import ListAPIView, CreateAPIView


class ShowTransactionAmount(ListAPIView):

    from .serializers import ShowTransactionDetailsSerializer

    queryset = TransactionDetails.objects.all()
    serializer_class = ShowTransactionDetailsSerializer
    filter_fields = ('category',)


class AddTransactionAmount(CreateAPIView):
    from .serializers import AddTransactionDetailsSerializer

    serializer_class = AddTransactionDetailsSerializer

    def perform_create(self, serializer):

        from contacts.models import ContactDetails

        contact_obj, created = ContactDetails.objects.get_or_create(name=serializer.validated_data['contact'],
                                                                    created_by=self.request.user)
        serializer.validated_data['contact'] = contact_obj
        serializer.save(created_by=self.request.user)


class ShowMode(ListAPIView):

    from .serializers import ShowModeSerializer
    from .models import TransactionModes
    from rest_framework.permissions import AllowAny

    permission_classes = (AllowAny, )
    queryset = TransactionModes.objects.all()
    serializer_class = ShowModeSerializer
    filter_backends = ()


def about(request):

    from django.shortcuts import render

    return render(request, 'transactions/about.html')
