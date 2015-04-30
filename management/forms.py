from django import forms
from django.forms.models import inlineformset_factory
from management.models import Location, SubLocation, Organization, ExchangeRate, Sector
from django.forms.models import BaseModelFormSet


class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Location
        exclude = ('id',)


class SubLocationForm(forms.ModelForm):
    #def __init__(self, *args, **kwargs):
    #    super(SubLocationForm, self).__init__(*args, **kwargs)
    #    self.fields['name'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = SubLocation
        exclude = ('id',)


class OrganizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Organization
        fields = ('name',)


class BaseSubLocationFormset(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseSubLocationFormset, self).__init__(*args, **kwargs)
        self.queryset = SubLocation.objects.none()


class BaseOrganizationFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseOrganizationFormSet, self).__init__(*args, **kwargs)
        self.queryset = Organization.objects.none()


class ExchangeRateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExchangeRateForm, self).__init__(*args, **kwargs)
        self.fields['rateToSOM'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = ExchangeRate
        exclude = ('dateSet',)


class BaseSectorFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseSectorFormSet, self).__init__(*args, **kwargs)
        self.queryset = Sector.objects.none()


class SectorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SectorForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['rows'] = '3'

    class Meta:
        model = Sector
        fields = ('name', 'description')

SubLocationFormset = inlineformset_factory(Location, SubLocation, fields=('name',), can_delete=True, extra=1,
                                           formset=BaseSubLocationFormset, form=SubLocationForm)
