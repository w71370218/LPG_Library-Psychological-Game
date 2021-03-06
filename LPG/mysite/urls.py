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
    path('game/',game, name='game'),
    path('app/',app, name='app'),
    path('test_img/',test_img, name='test_img'),
    path('administration/',administration, name='administration'),
    path('lucky_draw/',lucky_draw, name='lucky_draw'),
    path('booklist/',booklist, name='booklist'),
    path('pointrecord_list/',pointrecord_list, name='pointrecord_list'),
    path('testlist/',testlist, name='testlist'),
    path('recommend_list/',recommend_list, name='recommend_list'),
    path('single_new_test/',single_new_test, name='single_new_test'),
    re_path(r'^recommend/(?P<result>[0-9]+)/$', recommend_new, name='recommend_new'),
    path('upload_test_file/',upload_test_file, name='upload_test_file'),
    path('upload_booklist_file/',upload_booklist_file, name='upload_booklist_file'),
    path('process_result_from_client/',process_result_from_client, name='process_result_from_client'),
    path('proccess_single_test/',proccess_single_test,name='proccess_single_test'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^share_book/(?P<id>[0-9]+)/og/$', share_book, name='share_book'),
    re_path(r'^test/new/$', test_new, name='test_new'),
    re_path(r'^test/(?P<pk>[0-9]+)/edit/$', test_edit, name='test_edit'),
    re_path(r'^book/new/$', single_new_book, name='single_new_book'),
    re_path(r'^book/(?P<pk>[0-9]+)/edit/$', book_edit, name='book_edit'),
    re_path(r'^pointrecord/new/$', pointrecord_new, name='pointrecord_new'),
    re_path(r'^pointrecord/(?P<pk>[0-9]+)/edit/$', pointrecord_edit, name='pointrecord_edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
