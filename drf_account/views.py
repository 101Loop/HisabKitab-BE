from django_filters.rest_framework.backends import DjangoFilterBackend
from drfaddons.filters import IsOwnerFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView

from drf_account.models import BankMaster, BankAccount, DebitCard, CreditCard
from drf_account.serializers import (
    AddBankAccountSerializer,
    ShowBankAccountSerializer,
    AddDebitCardSerializer,
    UpdateCreditCardSerializer,
    ShowDebitCardSerializer,
    ShowCreditCardSerializer,
    AddCreditCardSerializer,
    ShowBankSerializer,
    UpdateBankAccountSerializer,
    UpdateDebitCardSerializer,
)
from drf_account.utils import get_bank_by_name


class AddBankAccountView(CreateAPIView):
    """
    This view will allow the user to add a new bank account.
    """

    serializer_class = AddBankAccountSerializer

    def perform_create(self, serializer):
        bank = serializer.validated_data["bank"]
        bank_master = get_bank_by_name(bank)
        if not bank_master:
            bank_master = BankMaster()
            bank_master.name = bank
            bank_master.created_by = self.request.user
            bank_master.save()
        serializer.validated_data["bank"] = bank_master
        serializer.save(created_by=self.request.user)


class ShowBankAccountView(ListAPIView):
    """
    This view will show the list of all bank account details.
    """

    serializer_class = ShowBankAccountSerializer
    queryset = BankAccount.objects.all().order_by("-create_date")


class AddDebitCardView(CreateAPIView):
    """
    This view will allow the user to add a new debit card.
    """

    serializer_class = AddDebitCardSerializer

    def perform_create(self, serializer):
        if (
            "account" in serializer.validated_data.keys()
            and serializer.validated_data["account"]
        ):
            account_obj = BankAccount.objects.get(
                pk=serializer.validated_data["account"]
            )
            serializer.validated_data["bank"] = account_obj.bank
        else:
            bank = serializer.validated_data["bank"]
            bank_master = get_bank_by_name(bank)
            if not bank_master:
                bank_master = BankMaster()
                bank_master.name = bank
                bank_master.created_by = self.request.user
                bank_master.save()
            serializer.validated_data["bank"] = bank_master
        serializer.save(created_by=self.request.user)


class ShowDebitCardView(ListAPIView):
    """
    This view will show the list of all debit cards.
    """

    serializer_class = ShowDebitCardSerializer
    queryset = DebitCard.objects.all().order_by("-create_date")


class AddCreditCardView(AddDebitCardView):
    """
    This view will allow the user to add a new credit card.
    """

    serializer_class = AddCreditCardSerializer


class ShowCreditCardView(ListAPIView):
    """
    This view will show the list of all credit cards.
    """

    serializer_class = ShowCreditCardSerializer
    queryset = CreditCard.objects.all().order_by("-create_date")


class ShowBankView(ListAPIView):
    """
    This view will show the list of all the banks.
    """

    serializer_class = ShowBankSerializer
    queryset = BankMaster.objects.all().order_by("-create_date")
    filter_backends = (DjangoFilterBackend,)


class UpdateBankAccountView(UpdateAPIView):
    """
    This view is to update bank account details.
    """

    queryset = BankAccount.objects.all()
    serializer_class = UpdateBankAccountSerializer
    filter_backends = (DjangoFilterBackend,)


class UpdateDebitCardView(UpdateAPIView):
    """
    This view is to update debit card details.
    """

    queryset = DebitCard.objects.all()
    serializer_class = UpdateDebitCardSerializer
    filter_backends = (DjangoFilterBackend,)


class UpdateCreditCardView(UpdateAPIView):
    """
    This view is to update Credit card details.
    """

    queryset = CreditCard.objects.all()
    serializer_class = UpdateCreditCardSerializer
    filter_backends = (DjangoFilterBackend, IsOwnerFilterBackend)
