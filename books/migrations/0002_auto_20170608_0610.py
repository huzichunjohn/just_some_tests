# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 06:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['id']},
        ),
    ]
