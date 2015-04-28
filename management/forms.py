from django import forms
from django.forms.models import inlineformset_factory
from management.models import Location, SubLocation, Organization, ExchangeRate, Sector
from django.forms.models import BaseModelFormSet


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ('id',)


class SubLocationForm(forms.ModelForm):
    class Meta:
        model = SubLocation
        exclude = ('id',)


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name',)


class BaseOrganizationFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseOrganizationFormSet, self).__init__(*args, **kwargs)
        self.queryset = Organization.objects.none()


class ExchangeRateForm(forms.ModelForm):
    class Meta:
        model = ExchangeRate
        exclude = ('dateSet',)


class BaseSectorFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseSectorFormSet, self).__init__(*args, **kwargs)
        self.queryset = Sector.objects.none()


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ('name', 'description')

SubLocationFormset = inlineformset_factory(Location, SubLocation, fields=('name',), can_delete=True, extra=1)
