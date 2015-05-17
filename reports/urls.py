from django.conf.urls import url
from reports.views import *


urlpatterns = [
    url(r'^$', project_list, name='dashboard'),
    url(r'^export-pdf/$', pdf_gen, name='gen-pdf')

]