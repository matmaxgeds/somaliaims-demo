from django.conf.urls import url
from reports.views import *


urlpatterns = [
    url(r'^$', project_list, name='dashboard'),
    url(r'^export-pdf/$', pdf_gen, name='gen-pdf'),
    url(r'^export-csv/$', csv_gen, name='gen-csv'),
    url(r'^export-xls/$', xls_gen, name='gen-xls'),
    url(r'^sector_report/', sector_report, name='sector-report'),
    url(r'^location_report/', location_report, name='location-report')
]