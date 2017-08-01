# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Project
from .forms import ProjectForm

class SuperUserMixin(PermissionRequiredMixin):
    def has_permission(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return False

class ProjectAdminMixin(PermissionRequiredMixin):
    def has_permission(self):
        project = self.get_object()
        if project.is_project_admin(self.request.user):
            return True
        return False

class ProjectMemberMixin(PermissionRequiredMixin):
    def has_permission(self):
        project = self.get_object()
        if project.is_project_member(self.request.user):
            return True
        return False

# class ProjectListView(LoginRequiredMixin, ListView):
class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'

class ProjectCreateView(LoginRequiredMixin, SuperUserMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_add.html'
    success_url = reverse_lazy('project_list')

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs['all_users'] =  User.objects.all()
        return kwargs

class ProjectEditView(LoginRequiredMixin, ProjectAdminMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_edit.html'
    success_url = reverse_lazy('project_list')

    def get_form_kwargs(self):
        kwargs = super(ProjectEditView, self).get_form_kwargs()
        kwargs['all_users'] =  User.objects.all()
        return kwargs

class ProjectDetailView(LoginRequiredMixin, ProjectMemberMixin, DetailView):
    model = Project
    template_name = 'project/project_detail.html'

class ProjectDeleteView(LoginRequiredMixin, ProjectAdminMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('project_list')
