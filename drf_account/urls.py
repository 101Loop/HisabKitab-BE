from django.urls import path
from . import views


app_name = 'drf_account'

urlpatterns = [
    # ex: api/users/login/
    path('bank/show/', views.ShowBankView.as_view(), name='Show Banks'),
    # ex: api/users/register/
    path('account/show/', views.ShowBankAccountView.as_view(), name='Show Bank Accounts'),
    # ex: api/users/loginotp/
    path('account/add/', views.AddBankAccountView.as_view(), name='Add Bank Account'),
]
