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

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLSz
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^admin/', admin.site.urls),
    url(r'^api/users/', include('users.urls')),
    url(r'^api/transactions/', include('drf_transaction.urls')),
    url(r'^api/contacts/', include('drf_contact.urls')),
    url(r'^api/feedback/', include('drf_feedback.urls')),
    url(r'^api/token/', include('fcm_notification.urls')),
    url(r'^api/account/', include('drf_account.urls')),
    url(r'^api/usersetting/', ChangeSettingsView.as_view(), name='Change User Settings'),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^$', about, name='about'),
]
