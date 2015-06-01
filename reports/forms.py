from django import forms
from management.models import Location, Sector, SubLocation
#from data_entry.models import LocationAllocation


def get_locations():
    return [[x.id, x.name] for x in Location.objects.all()]


def get_sectors():
    return [[x.id, x.name] for x in Sector.objects.all()]

# SUBLOCATIONS = [[x.id, x.name] for x in LocationAllocation.sublocations.all()]


def get_sublocations():
    return [[x.id, x.name] for x in SubLocation.objects.all()]


class LocationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['locations'] = forms.MultipleChoiceField(choices=get_locations(), label="")


class SectorForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SectorForm, self).__init__(*args, **kwargs)
        self.fields['sectors'] = forms.MultipleChoiceField(choices=get_sectors(), label="")


class SublocationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SublocationForm, self).__init__(*args, **kwargs)
        self.fields['sublocations'] = forms.MultipleChoiceField(choices=get_sublocations(), label="")


class SectorReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SectorReportForm, self).__init__(*args, **kwargs)
        self.fields['sector'] = forms.ChoiceField(choices=[('', '----------'), ] + get_sectors(), label='Sector',
                                                  widget=forms.Select(attrs={'onChange': "this.form.submit();"}))


class LocationReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LocationReportForm, self).__init__(*args, **kwargs)
        self.fields['location'] = forms.ChoiceField(choices=[('', '----------'), ] + get_locations(), label="Location",
                                 widget=forms.Select(attrs={'onChange': "this.form.submit();"}))