# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-29 03:32
from __future__ import unicode_literals

from django.db import migrations
from django.utils.text import slugify

def slugify_title(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    for post in Post.objects.all():
        post.slug = slugify(post.title)
        post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_slug'),
    ]

    operations = [
        migrations.RunPython(slugify_title),
    ]
