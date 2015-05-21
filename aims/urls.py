from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from .views import *

urlpatterns = [
    url(r'login_success/$', login_success, name='login_success'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^management/', include('management.urls')),
    url(r'^data-entry/', include('data_entry.urls', namespace='data-entry')),
    url(r'^reports/', include('reports.urls', namespace='reports')),
    url(r'^project_list/', include('reports.urls', namespace='projects')),
    url(r'^help/', include('help.urls', namespace='help')),
    url(r'^', include('home.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    #url(r'^$', 'aims.views.home', name='home'),


    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
