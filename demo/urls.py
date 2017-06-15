"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from hello import views
from books.views import book_list, book_export, book_detail, book_create, book_update, book_delete, add_custom_field

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^add_custom_field/$', add_custom_field, name="add_custom_field"),
    url(r'^books/', include('books.urls')),
    # url(r'^books/$', book_list, name="book_list"),
    # url(r'^books/export/$', book_export, name="book_export"),
    # url(r'^books/(?P<pk>\d+)/$', book_detail, name="book_detail"),
    # url(r'^books/(?P<pk>\d+)/update/$', book_update, name="book_update"),
    # url(r'^books/(?P<pk>\d+)/delete/$', book_delete, name="book_delete"),
    # url(r'^books/create/$', book_create, name="book_create"),
    url(r'^genres/$', views.show_genres, name='show_genres'),
    url(r'^application/add/$', views.ApplicationCreateView.as_view(), name='application-add'),
    url(r'^application/(?P<pk>\d+)/$', views.ApplicationDetailView.as_view(), name='application-detail'),
    url(r'^application/(?P<pk>\d+)/edit/$', views.ApplicationUpdateView.as_view(), name='application-edit'),
    url(r'^application/(?P<application_id>\d+)/setting/$', views.ApplicationSettingUpdateView.as_view(), name='application-setting-update'),
]
