from django import forms
from management.models import Location, Sector, SubLocation
from data_entry.models import LocationAllocation

LOCATIONS = [[x.id, x.name] for x in Location.objects.all()]

SECTORS = [[x.id, x.name] for x in Sector.objects.all()]

#SUBLOCATIONS = [[x.id, x.name] for x in LocationAllocation.sublocations.all()]

SUBLOCATIONS = [[x.id, x.name] for x in SubLocation.objects.all()]


class LocationForm(forms.Form):
    locations = forms.MultipleChoiceField(choices=LOCATIONS, label="")


class SectorForm(forms.Form):
    sectors = forms.MultipleChoiceField(choices=SECTORS, label="")


class SublocationForm(forms.Form):
    sublocations = forms.MultipleChoiceField(choices=SUBLOCATIONS, label="")
