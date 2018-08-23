"""Hisab Kitab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users.views import about
from usersettings.views import ChangeSettingsView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="HisabKitab API",
      default_version='v1',
      description="API based on DRF YASG for HisabKitab",
      contact=openapi.Contact(email="info@vitartha.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^api/users/', include('users.urls')),
    url(r'^api/transactions/', include('drf_transaction.urls')),
    url(r'^api/contacts/', include('drf_contact.urls')),
    url(r'^api/account/', include('drf_account.urls')),
    url(r'^api/usersetting/', ChangeSettingsView.as_view(), name='Change User Settings'),
    url(r'^munsiji/', include('munsiji.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLSz
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^', admin.site.urls),
]
