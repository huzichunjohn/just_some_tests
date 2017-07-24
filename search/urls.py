# -*- coding: utf-8 -*-
from django.conf.urls import url
from django_filters.views import FilterView
from .filters import UserFilter
# from .views import search

urlpatterns = [
    # url(r'^$', search, name='search'),
    url(r'^$', FilterView.as_view(filterset_class=UserFilter,
        template_name='search/user_list.html'), name='search'),
]