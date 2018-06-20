from django.urls import path
from . import views


app_name = 'transactions'

urlpatterns = [
    # ex: api/referral/add/
    path('add/', views.AddAmount.as_view(), name='Add-Referral-Code'),
    # ex: api/referral/show/
    path('show/', views.ShowAmount.as_view(), name='Show-Referral-Code'),
]
