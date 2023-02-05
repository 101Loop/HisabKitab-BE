from django.urls import path

from . import views

app_name = "drf_account"

urlpatterns = [
    # ex: api/account/bank/show/
    path("bank/show/", views.ShowBankView.as_view(), name="show_bank"),
    # ex: api/account/account/show/
    path(
        "account/show/", views.ShowBankAccountView.as_view(), name="show_bank_account"
    ),
    # ex: api/account/account/add/
    path("account/add/", views.AddBankAccountView.as_view(), name="add_bank_account"),
    # ex: api/account/debit/show/
    path("debit/show/", views.ShowDebitCardView.as_view(), name="show_debit_card"),
    # ex: api/account/debit/add/
    path("debit/add/", views.AddDebitCardView.as_view(), name="add_debit_card"),
    # ex: api/account/credit/show/
    path("credit/show/", views.ShowCreditCardView.as_view(), name="show_credit_card"),
    # ex: api/account/credit/add/
    path("credit/add/", views.AddCreditCardView.as_view(), name="add_credit_card"),
    # ex: api/account/account/update/pk/
    path(
        "account/update/<int:pk>/",
        views.UpdateBankAccountView.as_view(),
        name="update_bank_account",
    ),
    # ex: api/account/debit/update/pk/
    path(
        "debit/update/<int:pk>/",
        views.UpdateDebitCardView.as_view(),
        name="update_debit_card",
    ),
    # ex: api/account/credit/update/pk/
    path(
        "credit/update/<int:pk>/",
        views.UpdateCreditCardView.as_view(),
        name="update_credit_card",
    ),
]
