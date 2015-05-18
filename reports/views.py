from django.shortcuts import render_to_response
from .filters import ProjectFilter
from data_entry.models import Project, LocationAllocation, SectorAllocation
from django.template import RequestContext
from .forms import LocationForm, SectorForm, SublocationForm
from django.template.loader import get_template
from django.http import HttpResponse


def list_generator(request):
    allocated_projects = LocationAllocation.objects.values('project').distinct()
    pList = allocated_projects
    if request.GET.getlist('locations') == [] and request.GET.getlist('sectors') == [] and request.GET.getlist(
            'sublocations') == []:
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
    return filtered


def xls_gen(request):
    import xlwt
    from django.utils.six import moves
    filtered = list_generator(request)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=projectlist.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Projects")
    row_num = 0
    columns = [
        (u"Project Name", 6000),
        (u"Funders", 8000),
        (u"Duration", 6000),
        (u"Value", 6000),
        (u"Percentage Spent", 6000),

    ]
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in moves.xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]
    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in filtered:
        row_num += 1
        row = [
            obj.name,
            ','.join([x.name for x in obj.funders.all()]),
            obj.duration,
            obj.value,
            obj.percentage_spent,
        ]
        for col_num in moves.xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def csv_gen(request):
    import csv
    filtered = list_generator(request)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="projectlist.csv"'
    writer = csv.writer(response)
    head = csv.DictWriter(response, fieldnames=["Project Name", "Funders", "Duration", "Value", "Percentage Spent"],
                          delimiter=',')
    head.writeheader()
    for i in filtered:
        writer.writerow([i.name, ','.join([x.name for x in i.funders.all()]), i.duration, i.value,
                         i.percentage_spent])
    return response


def pdf_gen(request):
    import weasyprint
    filtered = list_generator(request)
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
    url = request.GET.urlencode()
    pdf_url = "http://127.0.0.1:8000/projects/export-pdf/?" + url
    csv_url = "http://127.0.0.1:8000/projects/export-csv/?" + url
    xls_url = "http://127.0.0.1:8000/projects/export-xls/?" + url
    page = request.get_full_path()
    exporters = False
    if "projects" in page:
        exporters = True
    filtered = list_generator(request)
    return render_to_response('reports/index.html', locals(), context_instance=RequestContext(request))
