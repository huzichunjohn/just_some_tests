# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import SimpleView, CartView, CreditCardView

urlpatterns = [
    url(r'^simple/$',SimpleView.as_view()),
    url(r'^cart/$', CartView.as_view()),
    url(r'^creditcard/$', CreditCardView.as_view()),
]