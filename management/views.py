from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from management.models import Location, Organization, Sector, ExchangeRate, SubLocation
from django.views.generic import ListView
from .forms import LocationForm, SubLocationFormset, OrganizationForm, BaseOrganizationFormSet, ExchangeRateForm, \
    BaseSectorFormSet, SectorForm, BaseSubLocationFormset
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from braces.views import GroupRequiredMixin


class ManagementDashboard(GroupRequiredMixin, ListView):
    model = Organization
    template_name = "management/index.html"
    queryset = Location.objects.all()
    group_required = [u"admin", u"management"]

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


class OrganizationCreate(GroupRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    group_required = [u"admin", u"management"]

    def get_context_data(self, **kwargs):
        context = super(OrganizationCreate, self).get_context_data(**kwargs)
        organizationFormset = modelformset_factory(Organization, form=OrganizationForm, fields=('name', ),
                                                   formset=BaseOrganizationFormSet)
        context['formset'] = organizationFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        sett = modelformset_factory(Organization, form=OrganizationForm, fields=('name', ), extra=1,
                                    formset=BaseOrganizationFormSet)
        formset = sett(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)

    def form_valid(self, formset):
        formset.save()
        return HttpResponseRedirect(reverse('dashboard'))

    def form_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset))


class OrganizationUpdate(GroupRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('dashboard')
    group_required = [u"admin", u"management"]

    def get_object(self, queryset=None):
        obj = Organization.objects.get(id=self.kwargs['pk'])
        return obj


class OrganizationDelete(GroupRequiredMixin, DeleteView):
    model = Organization
    success_url = reverse_lazy('dashboard')
    group_required = [u"admin", u"management"]


class LocationCreate(GroupRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    group_required = [u"admin", u"management"]

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


class LocationUpdate(GroupRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = "management/location_update_form.html"
    success_url = reverse_lazy('dashboard')
    group_required = [u"admin", u"management"]

    def get_context_data(self, **kwargs):
        context = super(LocationUpdate, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            sublocations = SubLocation.objects.filter(project=self.object).values()
            sub_formset = inlineformset_factory(Location, SubLocation, fields=('name',), can_delete=True, extra=len(
                sublocations), formset=BaseSubLocationFormset)
            context['formset'] = sub_formset(self.request.POST, self.request.FILES, initial=sublocations,
                                             prefix='document')
        else:
            sublocations = SubLocation.objects.filter(location=self.object).values()
            sub_formset = inlineformset_factory(Location, SubLocation, fields=('name',), can_delete=True, extra=len(
                sublocations), formset=BaseSubLocationFormset)
            context['formset'] = sub_formset(initial=sublocations, prefix='document')
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


class LocationDelete(GroupRequiredMixin, DeleteView):
    model = Location
    success_url = reverse_lazy('dashboard')
    group_required = [u"admin", u"management"]


class ExchangeRateUpdateView(GroupRequiredMixin, UpdateView):
    form_class = ExchangeRateForm
    success_url = reverse_lazy('dashboard')
    group_required = [u"admin", u"management"]

    def get_object(self, queryset=None):
        obj, created = ExchangeRate.objects.get_or_create()

        return obj


class SectorCreate(GroupRequiredMixin, CreateView):
    model = Sector
    form_class = SectorForm
    group_required = [u"admin", u"management"]

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


class SectorUpdate(GroupRequiredMixin, UpdateView):
    model = Sector
    form_class = SectorForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('dashboard')
    group_required = [u"admin", u"management"]

    def get_object(self, queryset=None):
        obj = Sector.objects.get(id=self.kwargs['pk'])
        return obj


class SectorDelete(GroupRequiredMixin, DeleteView):
    model = Sector
    success_url = reverse_lazy('dashboard')
    group_required = [u"admin", u"management"]

