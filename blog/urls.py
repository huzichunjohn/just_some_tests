# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers
from .views import ArticleView, export, simple_upload, generate_fake_data, get_articles, list, ArticleViewSet, FileUploadViewSet, fileupload

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'fileupload-list', FileUploadViewSet)

urlpatterns = [
    url(r'^$', ArticleView.as_view(), name='blog'),
    url(r'api/$', get_articles),
    url(r'api/', include(router.urls)),
    url(r'list/$', list),
    url(r'fileupload/$', fileupload),
    url(r'^export/$', export, name='export'),
    url(r'^import/$', simple_upload, name='import'),
    url(r'^fake/$', generate_fake_data, name='generate_fake_data'),
]