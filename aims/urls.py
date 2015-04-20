from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^', include('management.urls')),
    url(r'^', include('data_entry.urls')),
    url(r'^', include('home.urls')),
    #url(r'^$', 'aims.views.home', name='home'),


    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
