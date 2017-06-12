# -*- coding: utf-8 -*-
from django import forms
from extras.forms import BootstrapMixin, CustomFieldForm
from utilities.forms import CSVChoiceField
from .models import Book, BOOK_TYPES

class BookForm(BootstrapMixin, CustomFieldForm, forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'author', 'price', 'pages', 'book_type',)

class BookCSVForm(forms.ModelForm):
    book_type = CSVChoiceField(
        choices=BOOK_TYPES,
        help_text='Book type'
    )

    class Meta:
        model = Book
        fields = ('title', 'publication_date', 'author', 'price', 'pages', 'book_type')
