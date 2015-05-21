from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .views import *

urlpatterns = [
    url(r'^$', login_required(ProjectListView.as_view()), name='dashboard'),
    url(r'^project/create/$', login_required(ProjectCreateView.as_view()), name='project_add'),
    url(r'^project/update/(?P<pk>[^/]+)/$', login_required(ProjectUpdateView.as_view()), name='project_update'),
    url(r'^project/details/(?P<pk>[^/]+)/$', ProjectDetailView.as_view(), name='project_details'),
    url(r'^download/(?P<pk>[^/]+)/$', download_handler, name='download'),
    url(r'^project/delete/(?P<pk>[^/]+)/$', login_required(ProjectDelete.as_view()),
        name='project_delete'),
    #url(r'^sublocations/(?P<locationID>[^/]+)/', getSublocations, name='sublocations'),
    url(r'^sublocations/$', ajaxSublocations, name='ajax_sublocations'),
]
