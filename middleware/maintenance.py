from __future__ import absolute_import, print_function

from django.conf import settings
from django.http import HttpResponse

class ServicesUnavailableMiddleware(object):
    def process_request(self, request):
        if settings.MAINTENANCE:
            return HttpResponse('The application is currently in maintenance mode', status=503)
