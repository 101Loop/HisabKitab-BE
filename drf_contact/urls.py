from django.urls import re_path

from . import views

app_name = "drf_contact"


urlpatterns = [
    # ex: api/contacts/show/
    re_path(r"^show/", views.ShowContacts.as_view(), name="show_contact"),
    # ex: api/contacts/add/
    re_path(r"^add/", views.AddContacts.as_view(), name="add_contact"),
]
