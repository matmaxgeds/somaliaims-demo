from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .views import *

urlpatterns = [
    url(r'^$', login_required(ManagementDashboard.as_view()), name='dashboard'),
    url(r'^location/create/$', login_required(LocationCreate.as_view()), name='location_add'),
    #url(r'^location/update/(?P<uuid>\w+)/$', login_required(LocationUpdate.as_view()), name='location_update'),
    url(r'^location/update/(?P<pk>[^/]+)/$', login_required(LocationUpdate.as_view()), name='location_update'),
    url(r'^location/delete/(?P<pk>[^/]+)/$', login_required(LocationDelete.as_view()), name='location_delete'),
    url(r'^organization/create/$', login_required(OrganizationCreate.as_view()), name='organization_add'),
    url(r'^organization/update/(?P<pk>[^/]+)/$', login_required(OrganizationUpdate.as_view()), name='organization_update'),
    url(r'^organization/delete/(?P<pk>[^/]+)/$', login_required(OrganizationDelete.as_view()),
        name='organizations_delete'),
    url(r'^sector/create/$', login_required(SectorCreate.as_view()), name='sector_add'),
    url(r'^sector/update/(?P<pk>[^/]+)/$', login_required(SectorUpdate.as_view()), name='sector_update'),
    url(r'^sector/delete/(?P<pk>[^/]+)/$', login_required(SectorDelete.as_view()),
        name='sector_delete'),
    url(r'^exchange-rate/update/$', login_required(ExchangeRateUpdateView.as_view()), name='rate_update'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

