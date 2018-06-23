from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: api/contacts/
    url(r'', views.ShowContacts.as_view(), name='show-contact'),
    # url(r'', views.AddContacts.as_view(), name='add-contact'),

]
