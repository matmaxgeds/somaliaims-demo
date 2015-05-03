from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.views.generic.edit import FormView
from .forms import ContactForm


class HelpPageView(SuccessMessageMixin, FormView):
    """Help Page"""
    template_name = "help/help.html"
    form_class = ContactForm
    success_url = '/'
    success_message = "We have received your email. We will get back to you soon."

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

