from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from .models import Project, Spending, Contact
from management.models import SubLocation
from .forms import ProjectForm, LocationAllocationFormset, SectorAllocationFormset, UserOrganizationFormset, \
    DocumentFormset, SpendingForm, ContactForm


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('dashboard')

    def get_context_data(self, **kwargs):
        ctx = super(ProjectCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            ctx['form'] = ProjectForm(self.request.POST)
            ctx['form1'] = SpendingForm(self.request.POST, prefix='spending')
            ctx['form2'] = ContactForm(self.request.POST, prefix='contact')
            ctx['formset'] = LocationAllocationFormset(self.request.POST, prefix='location')
            ctx['formset1'] = SectorAllocationFormset(self.request.POST, prefix="sectors")
            ctx['formset2'] = UserOrganizationFormset(self.request.POST, prefix="user_organizations")
            ctx['formset3'] = DocumentFormset(self.request.POST, self.request.FILES, prefix="documents")
        else:
            ctx['form'] = ProjectForm()
            ctx['form1'] = SpendingForm(prefix='spending')
            ctx['form2'] = ContactForm(prefix='contact')
            ctx['formset'] = LocationAllocationFormset(prefix='location')
            ctx['formset1'] = SectorAllocationFormset(prefix="sectors")
            ctx['formset2'] = UserOrganizationFormset(prefix="user_organizations")
            ctx['formset3'] = DocumentFormset(prefix="documents")
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        form1 = ctx['form1']
        form2 = ctx['form2']
        formset = ctx['formset']
        formset1 = ctx['formset1']
        formset2 = ctx['formset2']
        formset3 = ctx['formset3']

        if formset.is_valid() and form.is_valid() and form1.is_valid() and form2.is_valid() and formset1.is_valid() \
                and formset2.is_valid() and formset3.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            form.save_m2m()
            objects = formset.save(commit=False)
            for object in objects:
                object.project = self.object
                object.save()
            formset.save_m2m()
            spending = form1.save(commit=False)
            spending.project = self.object
            spending.save()
            contact = form2.save(commit=False)
            contact.project = self.object
            contact.save()
            sectors = formset1.save(commit=False)
            for sector in sectors:
                sector.project = self.object
                sector.save()
            user_orgs = formset2.save(commit=False)
            for org in user_orgs:
                org.user = self.request.user
                org.project = self.object
                org.save()
            project = Project.objects.get(id=self.object.id)

            #doc_forms = DocumentFormset(self.request.POST, self.request.FILES, prefix="documents", instance=project)
            docs = formset3.save(commit=False)
            for doc in docs:
                doc.project = project
                doc.save()

            return redirect(self.get_success_url())

        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProjectListView(ListView):
    model = Project
    template_name = "data_entry/index.html"


def ajaxSublocations(request):
    html_string = ""
    if request.is_ajax():
        for sublocation in SubLocation.objects.filter(location=request.POST['location']):
            html_string += '<option value="%s">%s</option>' % (sublocation.pk, sublocation.name)

            return HttpResponse(html_string)


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('dashboard')

    def get_context_data(self, **kwargs):
        ctx = super(ProjectUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            ctx['form1'] = SpendingForm(self.request.POST, prefix='spending', instance=Spending.objects.get(project=self.object))
            ctx['form2'] = ContactForm(self.request.POST, prefix='contact', instance=Contact.objects.get(project=self.object))
            ctx['formset'] = LocationAllocationFormset(self.request.POST, prefix='location', instance=self.object)
            ctx['formset1'] = SectorAllocationFormset(self.request.POST, prefix="sectors", instance=self.object)
            ctx['formset2'] = UserOrganizationFormset(self.request.POST, prefix="user_organizations", instance=self.object)
            ctx['formset3'] = DocumentFormset(self.request.POST, self.request.FILES, prefix="documents", instance=self.object)
        else:
            ctx['form1'] = SpendingForm(prefix='spending', instance=Spending.objects.get(project=self.object))
            ctx['form2'] = ContactForm(prefix='contact', instance=Contact.objects.get(project=self.object))
            ctx['formset'] = LocationAllocationFormset(prefix='location', instance=self.object)
            ctx['formset1'] = SectorAllocationFormset(prefix="sectors", instance=self.object)
            ctx['formset2'] = UserOrganizationFormset(prefix="user_organizations", instance=self.object)
            ctx['formset3'] = DocumentFormset(prefix="documents", instance=self.object)
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        form1 = ctx['form1']
        form2 = ctx['form2']
        formset = ctx['formset']
        formset1 = ctx['formset1']
        formset2 = ctx['formset2']
        formset3 = ctx['formset3']

        if formset.is_valid() and form.is_valid() and form1.is_valid() and form2.is_valid() and formset1.is_valid() \
                and formset2.is_valid() and formset3.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            form.save_m2m()
            objects = formset.save(commit=False)
            for object in objects:
                object.project = self.object
                object.save()
            formset.save_m2m()
            spending = form1.save(commit=False)
            spending.project = self.object
            spending.save()
            contact = form2.save(commit=False)
            contact.project = self.object
            contact.save()
            sectors = formset1.save(commit=False)
            for sector in sectors:
                sector.project = self.object
                sector.save()
            user_orgs = formset2.save(commit=False)
            for org in user_orgs:
                org.user = self.request.user
                org.project = self.object
                org.save()
            project = Project.objects.get(id=self.object.id)

            docs = formset3.save(commit=False)
            for doc in docs:
                doc.project = project
                doc.save()

            return redirect(self.get_success_url())

        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('dashboard')