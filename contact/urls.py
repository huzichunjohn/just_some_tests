# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import home, user

urlpatterns = [
    url(r'^$', home),
    url(r'^user/$', user),
]
