from django.urls import path
from . import views


urlpatterns = [

    path('', views.AddFeedback.as_view(), name='add-feedback'),
]