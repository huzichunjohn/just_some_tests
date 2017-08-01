# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Project, Membership

class BootstrapMixin(forms.BaseForm):

    def __init__(self, *args, **kwargs):
        super(BootstrapMixin, self).__init__(*args, **kwargs)

        exempt_widgets = [forms.CheckboxInput, forms.ClearableFileInput, forms.FileInput, forms.RadioSelect]

        for field_name, field in self.fields.items():
            if field.widget.__class__ not in exempt_widgets:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join([css, 'form-control']).strip()
            if field.required:
                field.widget.attrs['required'] = 'required'
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label

class ProjectForm(BootstrapMixin, forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False
    )
    class Meta:
        model = Project
        fields = ['name', 'description']

    def __init__(self, all_users, *args, **kwargs):
        self.all_users = all_users
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['members'].queryset = self.all_users

    def save_members(self, project):
        Membership.objects.filter(project=project).delete()
        Membership.objects.bulk_create(
            [
                Membership(user=user, project=project)
                for user in self.cleaned_data['members']
            ]
        )

    def save(self, commit=True):
        project = super(ProjectForm, self).save()
        self.save_members(project)
        return project