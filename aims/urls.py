from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^', include('management.urls')),
    url(r'^', include('data_entry.urls')),
    url(r'^', include('home.urls')),
    #url(r'^$', 'aims.views.home', name='home'),


    url(r'^admin/', include(admin.site.urls)),
]
