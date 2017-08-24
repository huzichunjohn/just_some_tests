from __future__ import absolute_import, print_function

from django.http import HttpResponse
from django.core.urlresolvers import reverse, resolve, NoReverseMatch

import re
from maintenance.client import MaintenanceClient
client = MaintenanceClient()

class ServicesUnavailableMiddleware(object):
    def process_request(self, request):
        if client.get_maintenance_mode() == "on":
            try:
                off_url = reverse("maintenance:off")
                resolve(off_url)
                if off_url == request.path_info:
                    return None
            except NoReverseMatch:
                pass

            for url in ['^/accounts/login/$', '^/accounts/logout/$', '^/maintenance/']:
                re_url = re.compile(url)
                if re_url.match(request.path_info):
                    return None
            return HttpResponse('The application is currently in maintenance mode', status=503)
        else:
            return None