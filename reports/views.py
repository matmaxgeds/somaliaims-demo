from django.shortcuts import render_to_response
from .filters import ProjectFilter
from data_entry.models import Project, LocationAllocation, SectorAllocation
from django.template import RequestContext
from .forms import LocationForm, SectorForm, SublocationForm, SectorReportForm, LocationReportForm
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib.sites.models import Site
from management.models import Sector, Location


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
            row.insert(0, ','.join([x.name for x in obj.locations]))
        elif q and r and not s:
            row.insert(0, ','.join([x.name for x in obj.locations]))
            row.insert(1, ','.join([x.name for x in obj.sublocations]))
        elif q and r and s:
            row.insert(0, ','.join([x.name for x in obj.locations]))
            row.insert(1, ','.join([x.name for x in obj.sublocations]))
            row.insert(2, ','.join([x.name for x in obj.sectors]))
        elif not q and r and not s:
            row.insert(1, ','.join([x.name for x in obj.sublocations]))
        elif not q and not r and s:
            row.insert(2, ','.join([x.name for x in obj.sectors]))
        elif q and not r and s:
            row.insert(0, ','.join([x.name for x in obj.locations]))
            row.insert(1, ','.join([x.name for x in obj.sectors]))
        elif not q and r and s:
            row.insert(0, ','.join([x.name for x in obj.sublocations]))
            row.insert(1, ','.join([x.name for x in obj.sectors]))
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
            writer.writerow([i.name, ','.join([x.name for x in i.funders.all()]), i.duration, i.value,
                             i.percentage_spent])
    elif q and not r and not s:
        head = csv.DictWriter(response, fieldnames=["Locations", "Project Name", "Funders", "Duration", "Value",
                                                    "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x.name for x in i.locations]), i.name, ','.join([x.name for x in
                                                                                   i.funders.all()]), i.duration,
                             i.value,
                             i.percentage_spent])
    elif q and r and not s:
        head = csv.DictWriter(response, fieldnames=["Locations", "Sublocations", "Project Name", "Funders", "Duration",
                                                    "Value", "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x.name for x in i.locations]), ','.join([x for x in i.sublocations]),
                             i.name,
                             ','.join([x.name for x in i.funders.all()]),
                             i.duration, i.value, i.percentage_spent])
    elif q and r and s:
        head = csv.DictWriter(response, fieldnames=["Locations", "Sublocations", "Sectors", "Project Name", "Funders",
                                                    "Duration",
                                                    "Value", "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x.name for x in i.locations]), ','.join([x for x in i.sublocations]),
                             ','.join([x.name for x in i.sectors]),
                             i.name,
                             ','.join([x.name for x in i.funders.all()]),
                             i.duration, i.value, i.percentage_spent])
    elif not q and r and s:
        head = csv.DictWriter(response, fieldnames=["Sublocations", "Sectors", "Project Name", "Funders",
                                                    "Duration",
                                                    "Value", "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x.name for x in i.sublocations]),
                             ','.join([x.name for x in i.sectors]),
                             i.name,
                             ','.join([x.name for x in i.funders.all()]),
                             i.duration, i.value, i.percentage_spent])
    elif not q and not r and s:
        head = csv.DictWriter(response, fieldnames=["Sectors", "Project Name", "Funders",
                                                    "Duration",
                                                    "Value", "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x.name for x in i.sectors]),
                             i.name,
                             ','.join([x.name for x in i.funders.all()]),
                             i.duration, i.value, i.percentage_spent])
    elif not q and r and not s:
        head = csv.DictWriter(response, fieldnames=["Sublocations", "Project Name", "Funders",
                                                    "Duration",
                                                    "Value", "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in filtered:
            writer.writerow([','.join([x.name for x in i.sublocations]), i.name, ','.join([x.name for x in i.funders.all(

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


def sector_report(request):
    form = SectorReportForm()
    url = request.GET.urlencode()
    host = Site.objects.get_current().domain
    red_url = host + "/reports/sector/export-pdf?" + url
    csv_url = "/reports/sector/export-csv/?" + url
    xls_url = "/reports/sector/export-xls/?" + url
    pdf_url = """http://api.phantomjscloud.com/single/browser/v1/7935aba662a4bb6d9e7036bd23c049b94d779bca/?targetUrl={0}&loadImages=true&requestType=pdf&resourceUrlBlacklist=[]""".format(red_url)
    reports = True
    if request.GET.get('sector'):
        project_ids = SectorAllocation.objects.filter(sector=request.GET.get('sector')).values_list('project')
        projects = Project.objects.filter(id__in=list(set(project_ids)))
        allocation_dict = {}
        for project_id in project_ids:
            h = Project.objects.get(id=project_id)
            funders = h.funders.all()
            for funder in funders:
                try:
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] += 1
                except KeyError:
                    value = 1
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] = value
        sector = Sector.objects.get(id=request.GET.get('sector'))
        exporters = True
    return render_to_response("reports/sector_report.html", locals(), context_instance=RequestContext(request))


def sector_pdf(request):
    context = {}
    if request.GET.get('sector'):
        project_ids = SectorAllocation.objects.filter(sector=request.GET.get('sector')).values_list('project')
        projects = Project.objects.filter(id__in=list(set(project_ids)))
        allocation_dict = {}
        for project_id in project_ids:
            h = Project.objects.get(id=project_id)
            funders = h.funders.all()
            for funder in funders:
                try:
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] += 1
                except KeyError:
                    value = 1
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] = value
        sector = Sector.objects.get(id=request.GET.get('sector'))
        context['projects'] = projects
        context['sector'] = sector
        context['allocation_dict'] = allocation_dict
        template = get_template('reports/sector_export.html')
        html = template.render(RequestContext(request, context))
        response = HttpResponse(html)

    return response


def sector_csv(request):
    import csv
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    if request.GET.get('sector'):
        project_ids = SectorAllocation.objects.filter(sector=request.GET.get('sector')).values_list('project')
        projects = Project.objects.filter(id__in=list(set(project_ids)))
        allocation_dict = {}
        for project_id in project_ids:
            h = Project.objects.get(id=project_id)
            funders = h.funders.all()
            for funder in funders:
                try:
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] += 1
                except KeyError:
                    value = 1
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] = value
        head = csv.DictWriter(response, fieldnames=["Project Name", "Funders", "Implementers", "Duration", "Value",
                                                    "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in projects:
            writer.writerow([i.name, ','.join([x.name for x in i.funders.all()]), ','.join([x.name for x in
                                                                                            i.implementers.all()]), i.duration, i.value, i.percentage_spent])

    return response


def sector_xls(request):
    import xlwt
    from django.utils.six import moves

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=projectlist.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Projects")
    row_num = 0

    columns = [
        (u"Project Name", 6000),
        (u"Funders", 8000),
        (u"Implemeters", 8000),
        (u"Duration", 6000),
        (u"Value", 6000),
        (u"Percentage Spent", 6000),
    ]
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in moves.xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        ws.col(col_num).width = columns[col_num][1]
    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    if request.GET.get('sector'):
        project_ids = SectorAllocation.objects.filter(sector=request.GET.get('sector')).values_list('project')
        projects = Project.objects.filter(id__in=list(set(project_ids)))
        allocation_dict = {}
        for project_id in project_ids:
            h = Project.objects.get(id=project_id)
            funders = h.funders.all()
            for funder in funders:
                try:
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] += 1
                except KeyError:
                    value = 1
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] = value

    for obj in projects:
        row_num += 1
        row = [
            obj.name,
            ','.join([x.name for x in obj.funders.all()]),
            ','.join([x.name for x in obj.implementers.all()]),
            obj.duration,
            obj.value,
            obj.percentage_spent,
        ]

        for col_num in moves.xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def location_report(request):
    form = LocationReportForm()
    url = request.GET.urlencode()
    host = Site.objects.get_current().domain
    red_url = host + "/reports/location/export-pdf?" + url
    csv_url = "/reports/location/export-csv/?" + url
    xls_url = "/reports/location/export-xls/?" + url
    pdf_url = """http://api.phantomjscloud.com/single/browser/v1/7935aba662a4bb6d9e7036bd23c049b94d779bca/?targetUrl={0}&loadImages=true&requestType=pdf&resourceUrlBlacklist=[]""".format(red_url)
    reports = True
    if request.GET.get('location'):
        project_ids = LocationAllocation.objects.filter(location=request.GET.get('location')).values_list('project')
        projects = Project.objects.filter(id__in=list(set(project_ids)))
        allocation_dict = {}
        for project_id in project_ids:
            h = Project.objects.get(id=project_id)
            funders = h.funders.all()
            for funder in funders:
                try:
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] += 1
                except KeyError:
                    value = 1
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] = value
        location = Location.objects.get(id=request.GET.get('location'))
        exporters = True
    return render_to_response("reports/location_report.html", locals(), context_instance=RequestContext(request))


def loc_pdf(request):
    context = {}
    if request.GET.get('location'):
        project_ids = LocationAllocation.objects.filter(location=request.GET.get('location')).values_list('project')
        projects = Project.objects.filter(id__in=list(set(project_ids)))
        allocation_dict = {}
        for project_id in project_ids:
            h = Project.objects.get(id=project_id)
            funders = h.funders.all()
            for funder in funders:
                try:
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] += 1
                except KeyError:
                    value = 1
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] = value
        location = Location.objects.get(id=request.GET.get('location'))
        context['projects'] = projects
        context['location'] = location
        context['allocation_dict'] = allocation_dict
        template = get_template('reports/location_export.html')
        html = template.render(RequestContext(request, context))
        response = HttpResponse(html)

    return response


def loc_csv(request):
    import csv
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    if request.GET.get('location'):
        project_ids = LocationAllocation.objects.filter(location=request.GET.get('location')).values_list('project')
        projects = Project.objects.filter(id__in=list(set(project_ids)))
        allocation_dict = {}
        for project_id in project_ids:
            h = Project.objects.get(id=project_id)
            funders = h.funders.all()
            for funder in funders:
                try:
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] += 1
                except KeyError:
                    value = 1
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] = value
        head = csv.DictWriter(response, fieldnames=["Project Name", "Funders", "Implementers", "Duration", "Value",
                                                    "Percentage Spent"], delimiter=',')
        head.writeheader()
        for i in projects:
            writer.writerow([i.name, ','.join([x.name for x in i.funders.all()]), ','.join([x.name for x in
                                                                                            i.implementers.all()]), i.duration, i.value, i.percentage_spent])

    return response


def loc_xls(request):
    import xlwt
    from django.utils.six import moves

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=projectlist.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Projects")
    row_num = 0

    columns = [
        (u"Project Name", 6000),
        (u"Funders", 8000),
        (u"Implemeters", 8000),
        (u"Duration", 6000),
        (u"Value", 6000),
        (u"Percentage Spent", 6000),
    ]
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in moves.xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        ws.col(col_num).width = columns[col_num][1]
    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    if request.GET.get('location'):
        project_ids = LocationAllocation.objects.filter(location=request.GET.get('location')).values_list('project')
        projects = Project.objects.filter(id__in=list(set(project_ids)))
        allocation_dict = {}
        for project_id in project_ids:
            h = Project.objects.get(id=project_id)
            funders = h.funders.all()
            for funder in funders:
                try:
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] += 1
                except KeyError:
                    value = 1
                    key = str('_'.join(funder.name.split()))
                    allocation_dict[key] = value

    for obj in projects:
        row_num += 1
        row = [
            obj.name,
            ','.join([x.name for x in obj.funders.all()]),
            ','.join([x.name for x in obj.implementers.all()]),
            obj.duration,
            obj.value,
            obj.percentage_spent,
        ]

        for col_num in moves.xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response