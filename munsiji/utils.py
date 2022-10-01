import datetime

from dateutil import parser
from drf_contact.models import ContactDetail
from drf_transaction.models import TransactionDetail, TransactionMode


def add_trans(user, amount, name, trans_date, mode, category, purpose=None):
    contact_obj, create = ContactDetail.objects.get_or_create(
        name=name, created_by=user
    )

    td = TransactionDetail()
    td.created_by = user
    td.create_date = datetime.datetime.now()
    td.update_date = td.create_date
    td.amount = amount
    td.contact = contact_obj
    td.comments = purpose
    td.transaction_date = parser.parse(trans_date).date()
    td.category = category
    td.mode = TransactionMode.objects.get(pk=mode)
    td.save()
    return f"{td.created_by.name}, your {td.get_category_display()} transaction of {td.amount} amount toward {td.contact.name} done on {td.transaction_date} via {td.mode.mode} has been recorded."


def future_value(p: float, r: float, t: float, freq: str, lumpsum=False):
    frequency_factor = {"month": 12, "year": 1, "quarter": 4, "half": 2}
    r = r / (frequency_factor[freq]) / 100
    n = t * frequency_factor[freq]
    fv = ((1 + r) ** n) - 1
    fv = fv / r
    fv = fv * (1 + r)
    fv = fv * p
    return f"Your future value will be approximately {round(fv, 2)}."
