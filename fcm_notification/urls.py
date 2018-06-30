from django.urls import path
from . import views

urlpatterns = [
    # ex : api/token/
    path('', views.FCMTokenApi.as_view(), name = 'fcm-token'),
]