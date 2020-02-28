"""Hisab Kitab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.contrib import admin

from django.contrib.auth.views import LoginView

from usersettings.views import ChangeSettingsView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="HisabKitab API",
        default_version="v1",
        description="API based on DRF YASG for HisabKitab",
        contact=openapi.Contact(email="info@vitartha.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("accounts/login/", LoginView.as_view(), name="Login-User"),
    path("api/users/", include("users.urls")),
    path("api/transactions/", include("drf_transaction.urls")),
    path("api/contacts/", include("drf_contact.urls")),
    path("api/account/", include("drf_account.urls")),
    path("api/usersetting/", ChangeSettingsView.as_view(), name="Change User Settings"),
    path("munsiji/", include("munsiji.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=None),
        name="schema-json",
    ),
    re_path(
        "swagger/$",
        schema_view.with_ui("swagger", cache_timeout=None),
        name="schema-swagger-ui",
    ),
    re_path(
        "redoc/$", schema_view.with_ui("redoc", cache_timeout=None), name="schema-redoc"
    ),
    path("jet/", include("jet.urls", "jet")),  # Django JET URLSz
    path(
        "jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")
    ),  # Django JET dashboard URLS
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("", admin.site.urls),
]
