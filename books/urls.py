# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import book_list, book_export, book_detail, book_update, book_delete, book_create, BookImportView

urlpatterns = [
    url(r'^$', book_list, name="book_list"),
    url(r'^export/$', book_export, name="book_export"),
    url(r'^import/$', BookImportView.as_view(), name="book_import"),
    url(r'^(?P<pk>\d+)/$', book_detail, name="book_detail"),
    url(r'^(?P<pk>\d+)/update/$', book_update, name="book_update"),
    url(r'^(?P<pk>\d+)/delete/$', book_delete, name="book_delete"),
    url(r'^create/$', book_create, name="book_create"),
]