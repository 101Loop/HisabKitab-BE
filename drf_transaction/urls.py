from django.urls import path

from . import views


app_name = "drf_transaction"

urlpatterns = [
    # ex: api/transactions/add/
    path("add/", views.AddTransactionAmount.as_view(), name="add_transaction_amount"),
    # ex: api/transactions/show/
    path(
        "show/", views.ShowTransactionAmount.as_view(), name="show_transaction_amount"
    ),
    # ex: api/transactions/mode/show/
    path("mode/show/", views.ShowMode.as_view(), name="show_mode"),
    # ex: api/transactions/pk/delete/
    path(
        "<int:pk>/delete/",
        views.DeleteTransactionAmount.as_view(),
        name="delete_transaction_amount",
    ),
    # ex: api/transactions/pk/update/
    path(
        "<int:pk>/update/",
        views.UpdateTransactionAmount.as_view(),
        name="update_transaction_amount",
    ),
]
