from django.shortcuts import render_to_response
from .filters import ProjectFilter
from data_entry.models import Project, LocationAllocation, SectorAllocation
from django.template import RequestContext
from .forms import LocationForm, SectorForm, SublocationForm
from django.template.loader import get_template
from django.http import HttpResponse
import weasyprint


def pdf_gen(request):
    allocated_projects = LocationAllocation.objects.values('project').distinct()
    pList = allocated_projects
    import sys
    if request.GET.getlist('locations') == [] and request.GET.getlist('sectors') == [] and request.GET.getlist(
            'sublocations') == []:
        sys.stderr.write("1 called")
        allocated_projects = LocationAllocation.objects.values('project').distinct()
        pList = allocated_projects
    if request.GET.getlist('locations') != [] and request.GET.getlist('sectors') == [] and request.GET.getlist(
            'sublocations') == []:
        allocated_projects = LocationAllocation.objects.filter(
            location__in=request.GET.getlist('locations')).distinct().values('project')
        pList = allocated_projects
    if request.GET.getlist('sectors') != [] and request.GET.getlist('locations') == [] and request.GET.get(
            'sublocations') == []:
        allocated_sectors = SectorAllocation.objects.filter(
            sector__in=request.GET.getlist('sectors')).distinct().values('project')
        pList = allocated_sectors
    if request.GET.getlist('sublocations') != [] and request.GET.get('locations') == [] and request.GET.get(
            'sectors') == []:
        sublocations = LocationAllocation.objects.filter(
            sublocations__in=request.GET.getlist('sublocations')).distinct().values('project')
        pList = sublocations
    if request.GET.getlist('sectors') != [] and request.GET.getlist('locations') != [] and request.GET.getlist(
            'sublocations') == []:
        a = LocationAllocation.objects.filter(
            location__in=request.GET.getlist('locations')).distinct().values('project')
        b = SectorAllocation.objects.filter(sector__in=request.GET.getlist('sectors')).distinct().values(
            'project')
        for x, y in zip(a, b):
            x.update(y)
        pList = a
    if request.GET.getlist('sectors') != [] and request.GET.getlist('locations') != [] and request.GET.getlist(
            'sublocations') != []:
        a = LocationAllocation.objects.filter(
            location__in=request.GET.getlist('locations')).distinct().values('project')
        b = SectorAllocation.objects.filter(sector__in=request.GET.getlist('sectors')).distinct().values(
            'project')
        c = LocationAllocation.objects.filter(
            sublocations__in=request.GET.getlist('sublocations')).distinct().values('project')
        for x, y in zip(a, b):
            x.update(y)
        for x, y in zip(a, c):
            x.update(y)
        pList = a
    if request.GET.getlist('sectors') != [] and request.GET.getlist('sublocations') != [] and request.GET.getlist(
            'locations') == []:
        b = SectorAllocation.objects.filter(sector__in=request.GET.getlist('sectors')).distinct().values(
            'project')
        c = LocationAllocation.objects.filter(
            sublocations__in=request.GET.getlist('sublocations')).distinct().values('project')
        for x, y in zip(b, c):
            x.update(y)
        pList = b

    if request.GET.getlist('locations') != [] and request.GET.getlist('sublocations') != [] and request.GET.getlist(
            'sectors') == []:
        a = LocationAllocation.objects.filter(
            location__in=request.GET.getlist('locations')).distinct().values('project')
        c = LocationAllocation.objects.filter(
            sublocations__in=request.GET.getlist('sublocations')).distinct().values('project')
        for x, y in zip(a, c):
            x.update(y)
        pList = a
    filtered = ProjectFilter(request.GET, queryset=Project.objects.filter(id__in=pList))
    context = {'filtered': filtered}
    template = get_template('reports/report.html')
    html = template.render(RequestContext(request, context))
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response


def project_list(request):
    loc_form = LocationForm()
    sec_form = SectorForm()
    sub_form = SublocationForm()
    allocated_projects = LocationAllocation.objects.values('project').distinct()
    pList = allocated_projects
    url = request.GET.urlencode()
    pdf_url = "http://127.0.0.1:8000/reports/export-pdf/?" + url
    page = request.get_full_path()
    exporters = False
    if "reports" in page:
        exporters = True

    if request.GET.getlist('locations') != [] and request.GET.getlist('sectors') == [] and request.GET.getlist(
            'sublocations') == []:
        allocated_projects = LocationAllocation.objects.filter(
            location__in=request.GET.getlist('locations')).distinct().values('project')
        pList = allocated_projects
    if request.GET.getlist('sectors') != [] and request.GET.getlist('locations') == [] and request.GET.getlist(
            'sublocations') == []:
        allocated_sectors = SectorAllocation.objects.filter(
            sector__in=request.GET.getlist('sectors')).distinct().values('project')
        pList = allocated_sectors
    if request.GET.getlist('sublocations') != [] and request.GET.getlist('locations') == [] and request.GET.getlist(
            'sectors') == []:
        sublocations = LocationAllocation.objects.filter(
            sublocations__in=request.GET.getlist('sublocations')).distinct().values('project')
        pList = sublocations
    if request.GET.getlist('sectors') != [] and request.GET.getlist('locations') != [] and request.GET.getlist(
            'sublocations') == []:
        a = LocationAllocation.objects.filter(
            location__in=request.GET.getlist('locations')).distinct().values('project')
        b = SectorAllocation.objects.filter(sector__in=request.GET.getlist('sectors')).distinct().values(
            'project')
        for x, y in zip(a, b):
            x.update(y)
        pList = a
    if request.GET.getlist('sectors') != [] and request.GET.getlist('locations') != [] and request.GET.getlist(
            'sublocations') != []:
        a = LocationAllocation.objects.filter(
            location__in=request.GET.getlist('locations')).distinct().values('project')
        b = SectorAllocation.objects.filter(sector__in=request.GET.getlist('sectors')).distinct().values(
            'project')
        c = LocationAllocation.objects.filter(
            sublocations__in=request.GET.getlist('sublocations')).distinct().values('project')
        for x, y in zip(a, b):
            x.update(y)
        for x, y in zip(a, c):
            x.update(y)
        pList = a
    if request.GET.getlist('sectors') != [] and request.GET.getlist('sublocations') != [] and request.GET.getlist(
            'locations') == []:
        b = SectorAllocation.objects.filter(sector__in=request.GET.getlist('sectors')).distinct().values(
            'project')
        c = LocationAllocation.objects.filter(
            sublocations__in=request.GET.getlist('sublocations')).distinct().values('project')
        for x, y in zip(b, c):
            x.update(y)
        pList = b

    if request.GET.getlist('locations') != [] and request.GET.getlist('sublocations') != [] and request.GET.getlist(
            'sectors') == []:
        a = LocationAllocation.objects.filter(
            location__in=request.GET.getlist('locations')).distinct().values('project')
        c = LocationAllocation.objects.filter(
            sublocations__in=request.GET.getlist('sublocations')).distinct().values('project')
        for x, y in zip(a, c):
            x.update(y)
        pList = a
    import sys
    sys.stderr.write("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    sys.stderr.write(str(pList))
    filter = ProjectFilter(request.GET, queryset=Project.objects.filter(id__in=pList))
    return render_to_response('reports/index.html', locals(), context_instance=RequestContext(request))
