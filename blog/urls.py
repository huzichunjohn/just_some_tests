# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import ArticleView, generate_fake_data

urlpatterns = [
    url(r'^$', ArticleView.as_view(), name='blog'),
    url(r'^fake/$', generate_fake_data, name='generate_fake_data'),
]