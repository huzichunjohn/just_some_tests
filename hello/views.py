# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Application
from .forms import ApplicationForm

def index(request):
    return HttpResponse("hello world.")

def home(request):
    return HttpResponseRedirect(reverse('home'))

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        super(HomeView, self).get_context_data(**kwargs)

class ApplicationCreateView(CreateView):
    form_class = ApplicationForm
    template_name = 'add.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ApplicationCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('application-setting-update', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.language = form.cleaned_data['language']
        return super(ApplicationCreateView, self).form_valid(form)

class ApplicationUpdateView(UpdateView):
    form_class = ApplicationForm
    model = Application
    template_name = 'edit.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ApplicationUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('application-setting-update', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.language = form.cleaned_data['language']
        self.object.save()
        return super(ApplicationUpdateView, self).form_valid(form)

class ApplicationDetailView(DetailView):
    model = Application
    template_name = 'detail.html'

class ApplicationSettingUpdateView(UpdateView):
    template_name = 'setting.html'

    def get_application(self):
        return Application.objects.get(id=self.kwargs['application_id'])

    def get_object(self):
        application = self.get_application()
        return application.get_setting_instance()

    def get_form_class(self):
        return self.get_object().get_form_class()

    def get_success_url(self):
        return reverse('application-detail', args=[self.kwargs['application_id']])
