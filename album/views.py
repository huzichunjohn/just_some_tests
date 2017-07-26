# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import Photo
from .forms import PhotoForm

def photo_list(request):
    photos = Photo.objects.all()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'album/photo_list.html', {'form': form, 'photos': photos})

class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = reverse_lazy('photo_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        photo_path = os.path.join(settings.MEDIA_ROOT, self.object.file.name)
        if os.path.isfile(photo_path):
            try:
                os.remove(photo_path)
            except Exception:
                pass
        return HttpResponseRedirect(success_url)