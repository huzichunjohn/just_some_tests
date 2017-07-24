# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django import forms
import django_filters

class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    year_joined = django_filters.NumberFilter(name='date_joined', lookup_expr='year')
    year_joined__gt = django_filters.NumberFilter(name='date_joined', lookup_expr='year__gt')
    year_joined__lt = django_filters.NumberFilter(name='date_joined', lookup_expr='year__lt')
    groups = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'groups',]
        # fields = {
        #     'username': ['exact'],
        #     'first_name': ['icontains'],
        #     'last_name': ['exact'],
        #     'date_joined': ['year', 'year__gt', 'year__lt']
        # }
