# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from extras.models import CustomFieldModel, CustomFieldValue
from utilities.utils import csv_format

HARDCOVER = 1
PAPERBACK = 2
EBOOK = 3
BOOK_TYPES = (
    (HARDCOVER, 'Hardcover'),
    (PAPERBACK, 'Paperback'),
    (EBOOK, 'E-book'),
)

class Book(CustomFieldModel, models.Model):
    title = models.CharField(max_length=50)
    publication_date = models.DateField(null=True)
    author = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pages = models.IntegerField(blank=True, null=True)
    book_type = models.PositiveSmallIntegerField(choices=BOOK_TYPES)
    custom_field_values = GenericRelation(CustomFieldValue, content_type_field='obj_type', object_id_field='obj_id')
    csv_headers = [
        'title', 'publication_date', 'author', 'price', 'pages', 'book_type'
    ]
    class Meta:
        ordering = ['id']

    def to_csv(self):
        return csv_format([
            self.title,
            self.publication_date,
            self.author,
            self.price,
            self.pages,
            self.book_type
        ])
