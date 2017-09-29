# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=2000)
    date = models.DateTimeField()
    author = models.CharField(max_length=30)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title

class FileUpload(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, to_field='id')
    datafile = models.FileField()

class Post(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title