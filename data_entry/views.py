from django.http import HttpResponse
from django.shortcuts import redirect, HttpResponseRedirect, render_to_response
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from .models import Project, Spending, Contact, Document, LocationAllocation, SectorAllocation, UserOrganization, \
    SubPSGAllocation
from management.models import SubLocation
from .forms import ProjectForm, LocationAllocationFormset, SectorAllocationFormset, UserOrganizationFormset, \
    DocumentFormset, SpendingForm, ContactForm, BaseDocumentFormSet, SubPSGAllocationFormset
from django.forms.models import inlineformset_factory
from braces.views import GroupRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import DetailView
from filetransfers.api import serve_file
from django.shortcuts import get_object_or_404
from django.template.context import RequestContext
from django.template.loader import get_template
from django.contrib import messages
from .filters import ProjectFilter
from django.conf import settings
from django.db.models import Q


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'data_entry/project_details.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['project'] = self.object
        context['loc_allocations'] = LocationAllocation.objects.filter(project=self.object)
        context['subpsg_allocations'] = SubPSGAllocation.objects.filter(project=self.object)
        context['contact'] = Contact.objects.filter(project=self.object)
        context['sec_allocations'] = SectorAllocation.objects.filter(project=self.object)
        context['other_organizations'] = UserOrganization.objects.filter(project=self.object).distinct()
        context['documents'] = Document.objects.filter(project=self.object)
        context['exporters'] = True
        context['pdf_url'] = "/data-entry/project/export/" + str(self.object.id)
        return context


def project_export(request, pk):
    import weasyprint

    context = {}
    project = Project.objects.get(id=pk)
    context['project'] = project
    context['loc_allocations'] = LocationAllocation.objects.filter(project=project)
    context['contact'] = Contact.objects.filter(project=project)
    context['sec_allocations'] = SectorAllocation.objects.filter(project=project)
    context['other_organizations'] = UserOrganization.objects.filter(project=project).distinct()
    template = get_template('data_entry/project_export.html')
    html = template.render(RequestContext(request, context))
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response


def download_handler(request, pk):
    document = get_object_or_404(Document, id=pk)
    return serve_file(request, document.file, save_as=True)


class ProjectCreateView(GroupRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    group_required = [u"admin", u"data"]

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.kwargs = kwargs

        try:
            self.request.user.userprofile.organization.name
        except Exception:
            messages.warning(request, "You need to belong to an organization to add a project.")
            return HttpResponseRedirect(reverse('data-entry:dashboard'))

        return ProjectCreateView.dispatch(self, request, *args, **kwargs)

    def get_success_url(self):
        return redirect('/data-entry/')

    def get_context_data(self, **kwargs):
        ctx = super(ProjectCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            ctx['form'] = ProjectForm(self.request.POST)
            ctx['form1'] = SpendingForm(self.request.POST, prefix='spending')
            ctx['form2'] = ContactForm(self.request.POST, prefix='contact')
            ctx['formset'] = LocationAllocationFormset(self.request.POST, prefix='location')
            ctx['formset1'] = SectorAllocationFormset(self.request.POST, prefix="sectors")
            ctx['formset4'] = SubPSGAllocationFormset(self.request.POST, prefix='psg')
            ctx['formset2'] = UserOrganizationFormset(self.request.POST, prefix="user_organizations")
            ctx['formset3'] = DocumentFormset(self.request.POST, self.request.FILES, prefix="documents")
        else:
            ctx['form'] = ProjectForm()
            ctx['form1'] = SpendingForm(prefix='spending')
            ctx['form2'] = ContactForm(prefix='contact')
            ctx['formset'] = LocationAllocationFormset(prefix='location')
            ctx['formset1'] = SectorAllocationFormset(prefix="sectors")
            ctx['formset4'] = SubPSGAllocationFormset(prefix='psg')
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
        formset4 = ctx['formset4']

        if formset.is_valid() and form.is_valid() and form1.is_valid() and form2.is_valid() and formset1.is_valid() \
                and formset2.is_valid() and formset3.is_valid() and formset4.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            form.save_m2m()
            objects = formset.save(commit=False)
            for object in objects:
                object.project = self.object
                object.save()
            formset.save_m2m()
            psg_allocs = formset4.save(commit=False)
            for alloc in psg_allocs:
                alloc.project = self.object
                alloc.save()
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

            # doc_forms = DocumentFormset(self.request.POST, self.request.FILES, prefix="documents", instance=project)
            docs = formset3.save(commit=False)
            for doc in docs:
                doc.project = project
                doc.save()

            return HttpResponseRedirect(reverse('data-entry:dashboard'))

        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))



def ProjectListView(request):
    if request.GET.get('myProjects'):
        try:
            user_org = request.user.userprofile.organization.name
            queryset = Project.objects.filter(
                Q(funders__name__icontains=user_org) | Q(implementers__name__icontains=user_org)).distinct()
            if not queryset:
                projects = UserOrganization.objects.filter(name=user_org).values_list('project')
                queryset = Project.objects.filter(id__in=projects).distinct()
        except AttributeError:
            queryset = Project.objects.none()

    else:
        queryset = Project.objects.all()
    my_groups = request.user.groups.values_list('name', flat=True)
    if set(my_groups) & set(["admin", "data"]):
        pass
    else:
        return HttpResponseRedirect(settings.LOGIN_URL)
    filtered = ProjectFilter(request.GET, queryset=queryset)
    return render_to_response("data_entry/index.html", locals(), context_instance=RequestContext(request))


# TODO Kevin should work on the ajaxSublocations views. An ajaxSubPSGs view is also needed.
def ajaxSublocations(request):
    html_string = ""
    if request.is_ajax():
        for sublocation in SubLocation.objects.filter(location=request.POST['location']):
            html_string += '<option value="%s">%s</option>' % (sublocation.pk, sublocation.name)

            return HttpResponse(html_string)


class ProjectUpdateView(GroupRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "data_entry/project_update_form.html"
    group_required = [u"admin", u"data"]

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.object = self.get_object()

        _funders = self.object.funders.all().values_list('name')
        _implementers = self.object.implementers.all().values_list('name')
        _user_organizations = UserOrganization.objects.filter(project=self.object).values_list('name')
        try:
            _my_org = (self.request.user.userprofile.organization.name,)
        except Exception:
            messages.warning(request, "You need to belong to an organization to edit a project.")
            return HttpResponseRedirect(reverse('data-entry:dashboard'))

        if _my_org not in _funders and _my_org not in _implementers and _my_org not in _user_organizations:
            messages.warning(request,
                             "Sorry, your organization is not involved in this project. You have no edit permissions.")
            return HttpResponseRedirect(reverse('data-entry:dashboard'))
        return UpdateView.dispatch(self, request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not hasattr(self, '_object'):
            self._object = super(ProjectUpdateView, self).get_object()
        return self._object

    def get_context_data(self, **kwargs):
        ctx = super(ProjectUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            ctx['form1'] = SpendingForm(self.request.POST, prefix='spending',
                                        instance=Spending.objects.get(project=self.object))
            ctx['form2'] = ContactForm(self.request.POST, prefix='contact',
                                       instance=Contact.objects.get(project=self.object))
            ctx['formset'] = LocationAllocationFormset(self.request.POST, prefix='location', instance=self.object)
            ctx['formset1'] = SectorAllocationFormset(self.request.POST, prefix="sectors", instance=self.object)
            ctx['formset4'] = SubPSGAllocationFormset(self.request.POST, prefix='psg', instance=self.object)
            ctx['formset2'] = UserOrganizationFormset(self.request.POST, prefix="user_organizations",
                                                      instance=self.object)
            doc_values = Document.objects.filter(project=self.object).values()
            doc_formset = inlineformset_factory(Project, Document, fields=('name', 'file', 'link_to_document_website'), can_delete=True, extra=len(
                doc_values), formset=BaseDocumentFormSet)
            ctx['formset3'] = doc_formset(self.request.POST, self.request.FILES, initial=doc_values, prefix='document')
        else:

            ctx['form1'] = SpendingForm(prefix='spending', instance=Spending.objects.get(project=self.object))
            ctx['form2'] = ContactForm(prefix='contact', instance=Contact.objects.get(project=self.object))
            ctx['formset'] = LocationAllocationFormset(prefix='location', instance=self.object)
            ctx['formset1'] = SectorAllocationFormset(prefix="sectors", instance=self.object)
            ctx['formset4'] = SubPSGAllocationFormset(prefix='psg', instance=self.object)
            ctx['formset2'] = UserOrganizationFormset(prefix="user_organizations", instance=self.object)
            doc_values = Document.objects.filter(project=self.object).values()
            doc_formset = inlineformset_factory(Project, Document, fields=('name', 'file', 'link_to_document_website'), can_delete=True, extra=len(
                doc_values), formset=BaseDocumentFormSet)
            ctx['formset3'] = doc_formset(prefix='document', initial=doc_values)

        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        form1 = ctx['form1']
        form2 = ctx['form2']
        formset = ctx['formset']
        formset1 = ctx['formset1']
        formset2 = ctx['formset2']
        formset3 = ctx['formset3']
        formset4 = ctx['formset4']

        if formset.is_valid() and form.is_valid() and form1.is_valid() and form2.is_valid() and formset1.is_valid() \
                and formset2.is_valid() and formset3.is_valid() and formset4.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            form.save_m2m()
            objects = formset.save(commit=False)
            for object in objects:
                object.project = self.object
                object.save()
            sub_allocs = formset4.save(commit=False)
            for alloc in sub_allocs:
                alloc.project = self.object
                alloc.save()
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

            return HttpResponseRedirect(reverse('data-entry:dashboard'))

        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProjectDelete(GroupRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('data-entry:dashboard')
    group_required = [u"admin", u"data"]
