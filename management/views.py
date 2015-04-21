from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from management.models import Location, Organization, Sector, ExchangeRate
from django.views.generic import ListView
from .forms import LocationForm, SubLocationFormset, OrganizationForm, BaseOrganizationFormSet, ExchangeRateForm, \
    BaseSectorFormSet, SectorForm
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelformset_factory


class ManagementDashboard(ListView):
    model = Organization
    template_name = "management/index.html"
    queryset = Location.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ManagementDashboard, self).get_context_data(**kwargs)
        context['organizations'] = Organization.objects.all()
        context['sectors'] = Sector.objects.all()
        try:
            context['exchange_rate'] = ExchangeRate.objects.get()
        except ExchangeRate.DoesNotExist:
            pass
        return context

    def dispatch(self, *args, **kwargs):
        return super(ManagementDashboard, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Location.objects.all()


class OrganizationCreate(CreateView):
    model = Organization
    form_class = OrganizationForm

    def get_context_data(self, **kwargs):
        context = super(OrganizationCreate, self).get_context_data(**kwargs)
        organizationFormset = modelformset_factory(Organization, form=OrganizationForm, fields=('name', ), formset=BaseOrganizationFormSet)
        context['formset'] = organizationFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        set = modelformset_factory(Organization, form=OrganizationForm, fields=('name', ), extra=1,
                                   formset=BaseOrganizationFormSet)
        formset = set(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)

    def form_valid(self, formset):
        formset.save()
        return HttpResponseRedirect(reverse('dashboard'))

    def form_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset))


class OrganizationUpdate(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        obj = Organization.objects.get(id=self.kwargs['pk'])
        return obj


class OrganizationDelete(DeleteView):
    model = Organization
    success_url = reverse_lazy('dashboard')


class LocationCreate(CreateView):
    model = Location
    form_class = LocationForm

    def get_context_data(self, **kwargs):
        context = super(LocationCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = SubLocationFormset(self.request.POST)
        else:
            context['formset'] = SubLocationFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return HttpResponseRedirect(reverse('dashboard'))  # assuming your model has ``get_absolute_url`` defined.
        else:
            return self.render_to_response(self.get_context_data(form=form))


class LocationUpdate(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = "management/location_update_form.html"
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super(LocationUpdate, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['formset'] = SubLocationFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = SubLocationFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            form.save()
            formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LocationUpdate, self).form_valid(form)


class LocationDelete(DeleteView):
    model = Location
    success_url = reverse_lazy('dashboard')


class ExchangeRateUpdateView(UpdateView):
    form_class = ExchangeRateForm
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        obj, created = ExchangeRate.objects.get_or_create()

        return obj


class SectorCreate(CreateView):
    model = Sector
    form_class = SectorForm

    def get_context_data(self, **kwargs):
        context = super(SectorCreate, self).get_context_data(**kwargs)
        sectorFormset = modelformset_factory(Sector, form=SectorForm, fields=('name', 'description'),
                                        formset=BaseSectorFormSet)
        context['formset'] = sectorFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        set = modelformset_factory(Sector, form=SectorForm, fields=('name', 'description'), extra=1,
                                   formset=BaseSectorFormSet)
        formset = set(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)

    def form_valid(self, formset):
        formset.save()
        return HttpResponseRedirect(reverse('dashboard'))

    def form_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset))


class SectorUpdate(UpdateView):
    model = Sector
    form_class = SectorForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        obj = Sector.objects.get(id=self.kwargs['pk'])
        return obj


class SectorDelete(DeleteView):
    model = Sector
    success_url = reverse_lazy('dashboard')

