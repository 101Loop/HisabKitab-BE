from django.urls import path
from . import views


urlpatterns = [

    # ex: api/feedback/
    path('', views.AddFeedback.as_view(), name='add-feedback'),
]