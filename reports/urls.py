from django.conf.urls import url
from reports.views import *


urlpatterns = [
    url(r'^$', project_list, name='dashboard'),
    url(r'^export-pdf/$', pdf_gen, name='gen-pdf'),
    url(r'^export-csv/$', csv_gen, name='gen-csv'),
    url(r'^export-xls/$', xls_gen, name='gen-xls'),
    url(r'^sector/export-pdf/$', sector_pdf, name='sec-pdf'),
    url(r'^sector/export-csv/$', sector_csv, name='sec-csv'),
    url(r'^sector/export-xls/$', sector_xls, name='sec-xls'),
    url(r'^sector_report/', sector_report, name='sector-report'),
    url(r'^location_report/', location_report, name='location-report'),
    url(r'^location/export-pdf/$', loc_pdf, name='loc-pdf'),
    url(r'^location/export-csv/$', loc_csv, name='loc-csv'),
    url(r'^location/export-xls/$', loc_xls, name='loc-xls'),
]