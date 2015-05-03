from django.shortcuts import render_to_response
from django.template.context import RequestContext


def home(request):
    """Home page"""
    return render_to_response("home/homepage.html", locals(), context_instance=RequestContext(request))

