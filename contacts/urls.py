from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'', views.ShowContacts.as_view(), name='contact'),

]
