# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

from .forms import SimpleForm, CartForm, CreditCardForm

class SimpleView(FormView):
    form_class = SimpleForm
    template_name = 'foo/index.html'
    success_url = reverse_lazy('home')

class CartView(FormView):
    form_class = CartForm
    template_name = 'foo/index.html'
    success_url = reverse_lazy('home')

class CreditCardView(FormView):
    form_class = CreditCardForm
    template_name = 'foo/index.html'
    success_url = reverse_lazy('home')
