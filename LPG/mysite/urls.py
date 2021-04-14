"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from trips.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('app/',app, name='app'),
    path('administration/',administration, name='administration'),
    path('process_result_from_client/',process_result_from_client, name='process_result_from_client'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^test/new/$', test_new, name='test_new'),
    re_path(r'^test/(?P<pk>[0-9]+)/edit/$', test_edit, name='test_edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
