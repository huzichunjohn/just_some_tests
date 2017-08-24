# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse

from maintenance.client import MaintenanceClient
client = MaintenanceClient()

def index(request):
    maintenance = client.get_maintenance_mode()
    return render(request, 'maintenance/index.html', {"maintenance": maintenance})

@login_required
def on(request):
    if request.user.is_superuser:
        client.set_maintainance_mode('on')
        return HttpResponseRedirect(reverse('maintenance:index'))
    return HttpResponseForbidden("Only super user can modify.")

@login_required
def off(request):
    if request.user.is_superuser:
        client.set_maintainance_mode('off')
        return HttpResponseRedirect(reverse('maintenance:index'))
    return HttpResponseForbidden("Only super user can modify.")
