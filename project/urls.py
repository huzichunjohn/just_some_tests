# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import ProjectListView, ProjectCreateView, ProjectEditView, ProjectDetailView, ProjectDeleteView

urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name='project_list'),
    url(r'^add/$', ProjectCreateView.as_view(), name='project_add'),
    url(r'^(?P<pk>\d+)/$', ProjectDetailView.as_view(), name='project_detail'),
    url(r'^(?P<pk>\d+)/edit/$', ProjectEditView.as_view(), name='project_edit'),
    url(r'^(?P<pk>\d+)/delete/$', ProjectDeleteView.as_view(), name='project_delete'),
]