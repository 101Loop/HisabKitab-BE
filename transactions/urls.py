from django.urls import path
from . import views


app_name = 'transactions'

urlpatterns = [
    # ex: api/transactions/add/
    path('add/', views.AddTransactionAmount.as_view(), name='Add-Transactions-Amount'),
    # ex: api/transactions/show/
    path('show/', views.ShowTransactionAmount.as_view(), name='Show-Transactions-Amount'),
    # ex: api/transactions/mode/show/
    path('mode/show/', views.ShowMode.as_view(), name='Show-Mode'),
]
