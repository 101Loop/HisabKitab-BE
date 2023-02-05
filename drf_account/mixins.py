from typing import Optional

from drf_account.models import BankMaster
from drf_account.utils import get_bank_by_name


class CreateBankAccountMixin:
    def get_or_create_bank(self, bank_name: str) -> BankMaster:
        """
        This function will create a new bank account using the serializer.
        """
        bank_master: Optional[BankMaster] = get_bank_by_name(bank_name)
        if not bank_master:
            bank_master = BankMaster()
            bank_master.name = bank_name
            bank_master.created_by = self.request.user
            bank_master.save()

        return bank_master
