from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import TemplateView


def home(request):
    """Home page"""
    return render_to_response("home/homepage.html", locals(), context_instance=RequestContext(request))


class HelpPageView(TemplateView):
    """Help Page"""
    template_name = "home/help.html"
