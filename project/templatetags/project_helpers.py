# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter()
def is_project_admin(project, user):
    if user.is_anonymous():
        return False
    return project.is_project_admin(user)

@register.filter()
def is_project_member(project, user):
    if user.is_anonymous():
        return False
    return project.is_project_member(user)