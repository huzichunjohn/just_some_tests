# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin):
    pass
