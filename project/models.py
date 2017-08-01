# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name="projects", blank=True,
                                     through="Membership", through_fields=("project", "user"))

    def is_project_member(self, user):
        if user.is_superuser:
            return True

        try:
            membership = Membership.objects.get(user=user, project=self)
        except Membership.DoesNotExist:
            return False
        return True

    def is_project_admin(self, user):
        if user.is_superuser:
            return True

        try:
            membership = Membership.objects.get(user=user, project=self)
        except Membership.DoesNotExist:
            return False

        if membership and membership.is_admin:
            return True
        return False

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(User, related_name='memberships')
    project = models.ForeignKey(Project, related_name='memberships')
    is_admin = models.BooleanField(default=False)
