from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect, render_to_response, redirect
from django.template.context import RequestContext
from django.views.generic.edit import FormView

from .forms import ContactForm


def home(request):
    """Home page"""
    return render_to_response("home/homepage.html", locals(), context_instance=RequestContext(request))


class HelpPageView(FormView):
    """Help Page"""
    template_name = "home/help.html"
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        if name and email and message:
            send_mail(
                "[AIMS Contact Form] New Message from {}".format(name),
                message,
                email,
                ['somali.aims@gmail.com'],
                fail_silently=False)
        return super(HelpPageView, self).form_valid(form)
