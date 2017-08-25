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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

from hello import views
from books.views import book_list, book_export, book_detail, book_create, book_update, book_delete, add_custom_field

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name="home"),
    url(r'^foo/', include('foo.urls')),
    url(r'^maintenance/', include('maintenance.urls', namespace='maintenance')),
    url(r'^accounts/login/$', login, name='login', kwargs={'template_name': 'login.html'}),
    url(r'^accounts/logout/$', logout, name='logout', kwargs={'next_page': '/accounts/login/'}),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    # url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^add_custom_field/$', add_custom_field, name="add_custom_field"),
    url(r'^books/', include('books.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^photos/', include('photos.urls', namespace='photos')),
    url(r'^album/', include('album.urls')),
    url(r'^project/', include('project.urls')),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
