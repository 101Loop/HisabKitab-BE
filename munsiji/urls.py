from django.urls import path

from . import views


app_name = "munsiji"

urlpatterns = [
    # ex: api/restaurant/show/item/
    path("webhook/", views.MunsiJiCall.as_view(), name="WebHook-DialogFlow"),
]
