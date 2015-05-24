from django.shortcuts import render_to_response
from .filters import ProjectFilter
from data_entry.models import Project, LocationAllocation, SectorAllocation
from django.template import RequestContext
from .forms import LocationForm, SectorForm, SublocationForm
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib.sites.models import Site


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

    q = request.GET.getlist('locations')
    r = request.GET.getlist('sublocations')
    s = request.GET.getlist('sectors')

    columns = [
        (u"Project Name", 6000),
        (u"Funders", 8000),
        (u"Duration", 6000),
        (u"Value", 6000),
        (u"Percentage Spent", 6000),
    ]

    if not q and not r and not s:
        pass
    elif q and not r and not s:
        columns.insert(0, (u"Locations", 12000))
    elif q and r and not s:
        columns.insert(0, (u"Locations", 12000))
        columns.insert(1, (u"Sublocations", 12000))
    elif q and r and s:
        columns.insert(0, (u"Locations", 12000))
        columns.insert(1, (u"Sublocations", 12000))
        columns.insert(2, (u"Sectors", 12000))
    elif not q and r and not s:
        columns.insert(1, (u"Sublocations", 12000))
    elif not q and not r and s:
        columns.insert(2, (u"Sectors", 12000))
    elif q and not r and s:
        columns.insert(0, (u"Locations", 12000))
        columns.insert(1, (u"Sectors", 12000))
    elif not q and r and s:
        columns.insert(0, (u"Sublocations", 12000))
        columns.insert(1, (u"Sectors", 12000))

    import sys

    sys.stderr.write(str(columns))

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
        if not q and not r and not s:
            pass
        elif q and not r and not s:
            row.insert(0, ','.join([x for x in obj.locations]))
        elif q and r and not s:
            row.insert(0, ','.join([x for x in obj.locations]))
            row.insert(1, ','.join([x for x in obj.sublocations]))
        elif q and r and s:
            row.insert(0, ','.join([x for x in obj.locations]))
            row.insert(1, ','.join([x for x in obj.sublocations]))
            row.insert(2, ','.join([x for x in obj.sectors]))
        elif not q and r and not s:
            row.insert(1, ','.join([x for x in obj.sublocations]))
        elif not q and not r and s:
            row.insert(2, ','.join([x for x in obj.sectors]))
        elif q and not r and s:
            row.insert(0, ','.join([x for x in obj.locations]))
            row.insert(1, ','.join([x for x in obj.sectors]))
        elif not q and r and s:
            row.insert(0, ','.join([x for x in obj.sublocations]))
            row.insert(1, ','.join([x for x in obj.sectors]))
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
    q = request.GET.getlist('locations')
    r = request.GET.getlist('sublocations')
    s = request.GET.getlist('sectors')
    if not q and not r and not s:
        head = csv.DictWriter(response, fieldnames=["Project Name", "Funders", "Duration", "Value", "Percentage Spent"],
                              delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([i.name, ','.join([x for x in i.funders.all()]), i.duration, i.value,
                             i.percentage_spent])
    elif q and not r and not s:
        head = csv.DictWriter(response, fieldnames=["Locations", "Project Name", "Funders", "Duration", "Value",
                                                    "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x for x in i.locations]), i.name, ','.join([x.name for x in
                                                                                   i.funders.all()]), i.duration,
                             i.value,
                             i.percentage_spent])
    elif q and r and not s:
        head = csv.DictWriter(response, fieldnames=["Locations", "Sublocations", "Project Name", "Funders", "Duration",
                                                    "Value", "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x for x in i.locations]), ','.join([x for x in i.sublocations]),
                             i.name,
                             ','.join([x.name for x in i.funders.all()]),
                             i.duration, i.value, i.percentage_spent])
    elif q and r and s:
        head = csv.DictWriter(response, fieldnames=["Locations", "Sublocations", "Sectors", "Project Name", "Funders",
                                                    "Duration",
                                                    "Value", "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x for x in i.locations]), ','.join([x for x in i.sublocations]),
                             ','.join([x for x in i.sectors]),
                             i.name,
                             ','.join([x.name for x in i.funders.all()]),
                             i.duration, i.value, i.percentage_spent])
    elif not q and r and s:
        head = csv.DictWriter(response, fieldnames=["Sublocations", "Sectors", "Project Name", "Funders",
                                                    "Duration",
                                                    "Value", "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x for x in i.sublocations]),
                             ','.join([x for x in i.sectors]),
                             i.name,
                             ','.join([x.name for x in i.funders.all()]),
                             i.duration, i.value, i.percentage_spent])
    elif not q and not r and s:
        head = csv.DictWriter(response, fieldnames=["Sectors", "Project Name", "Funders",
                                                    "Duration",
                                                    "Value", "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x for x in i.sectors]),
                             i.name,
                             ','.join([x.name for x in i.funders.all()]),
                             i.duration, i.value, i.percentage_spent])
    elif not q and r and not s:
        head = csv.DictWriter(response, fieldnames=["Sublocations", "Project Name", "Funders",
                                                    "Duration",
                                                    "Value", "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x for x in i.sublocations]), i.name, ','.join([x.name for x in i.funders.all(

            )]), i.duration, i.value, i.percentage_spent])

    return response


def pdf_gen(request):
    import weasyprint

    filtered = list_generator(request)
    q = request.GET.getlist('locations')
    context = {}
    if not q:
        pass
    else:
        context['loc_display'] = True
    r = request.GET.getlist('sublocations')
    if not r:
        pass
    else:
        context['sub_display'] = True
    s = request.GET.getlist('sectors')
    if not s:
        pass
    else:
        context['sec_display'] = True
    context['filtered'] = filtered
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
    host = Site.objects.get_current().domain
    pdf_url = "/project_list/export-pdf/?" + url
    csv_url = "/project_list/export-csv/?" + url
    xls_url = "/project_list/export-xls/?" + url
    page = request.get_full_path()
    exporters = False
    if "project_list" in page:
        exporters = True
    filtered = list_generator(request)
    q = request.GET.getlist('locations')
    if not q:
        pass
    else:
        loc_display = True
    r = request.GET.getlist('sublocations')
    if not r:
        pass
    else:
        sub_display = True
    s = request.GET.getlist('sectors')
    if not s:
        pass
    else:
        sec_display = True

    return render_to_response('reports/index.html', locals(), context_instance=RequestContext(request))
