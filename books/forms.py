# -*- coding: utf-8 -*-
from django import forms
from extras.forms import BootstrapMixin, CustomFieldForm
from .models import Book

class BookForm(BootstrapMixin, CustomFieldForm, forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'author', 'price', 'pages', 'book_type',)
