# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import photo_list, PhotoDeleteView

urlpatterns = [
    url(r'^$', photo_list, name='photo_list'),
    url(r'^(?P<pk>\d+)/delete/$', PhotoDeleteView.as_view(), name='photo_delete'),
]