# -*- coding: utf-8 -*-
import django_tables2 as tables
from utilities.tables import BaseTable

from .models import Book

class BookTable(BaseTable):

    class Meta(BaseTable.Meta):
        model = Book
        field = ('title', 'publication_date', 'author', 'price', 'pages', 'book_type')
