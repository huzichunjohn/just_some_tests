# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Article, FileUpload

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'body', 'date', 'author')

class FileUploadSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = FileUpload
        fields = ('created', 'datafile', 'owner')
        read_only_fields = ('created', 'owner')
