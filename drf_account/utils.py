from typing import Optional

from django.db.models import QuerySet

from drf_account.models import BankMaster


def get_bank_by_name(name: str) -> Optional[BankMaster]:
    """
    This function checks if the bank exists in the database or not.
    Parameters
    ----------
    name: str

    Returns
    -------
    str
        The name of the bank if it exists otherwise None.
    Examples
    --------
    To check if 'Axis Bank' bank is already present in Database or not.
    >>> print(get_bank_by_name('Axis Bank'))
    Axis Bank
    To check if 'Central Bank' bank is already present in Database or not.
    >>> print(get_bank_by_name('Central Bank'))
    None
    """
    try:
        bank_master: BankMaster = BankMaster.objects.get(name=name)
    except BankMaster.DoesNotExist:
        regex = f"{name}"
        bank_master: QuerySet = BankMaster.objects.filter(aliases__iregex=regex).first()
        return bank_master or None

    return bank_master
