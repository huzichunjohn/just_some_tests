# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import index, on, off

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^on/$', on, name='on'),
    url(r'^off/$', off, name='off'),
]