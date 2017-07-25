# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload')
]