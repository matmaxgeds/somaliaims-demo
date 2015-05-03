from django.shortcuts import render_to_response
from .filters import ProjectFilter
from data_entry.models import Project


def project_list(request):
    projects = ProjectFilter(request.GET, queryset=Project.objects.all())
    return render_to_response('reports/index.html', {'filter': projects})
