from django import forms
from django.forms.models import inlineformset_factory
from management.models import Location, SubLocation, Organization, ExchangeRate, Sector, PSG, SubPSG
from django.forms.models import BaseModelFormSet, BaseInlineFormSet


class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Location
        exclude = ('id',)


class SubLocationForm(forms.ModelForm):
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


class BaseSubLocationFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseSubLocationFormset, self).__init__(*args, **kwargs)
        self.queryset = SubLocation.objects.none()


class BaseSubPSGFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseSubPSGFormset, self).__init__(*args, **kwargs)
        self.queryset = SubPSG.objects.none()


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


class PSGForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PSGForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = PSG
        exclude = ('id',)


class SubPSGForm(forms.ModelForm):
    class Meta:
        model = SubPSG
        exclude = ('id', 'description',)


SubLocationFormset = inlineformset_factory(Location, SubLocation, fields=('name',), can_delete=True, extra=1,
                                           formset=BaseSubLocationFormset, form=SubLocationForm)

SubPSGFormset = inlineformset_factory(PSG, SubPSG, fields=('name',), can_delete=True, extra=1,
                                      formset=BaseSubPSGFormset, form=PSGForm)
