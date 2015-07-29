from django.forms import ModelForm
from .models import Project, LocationAllocation, SectorAllocation, UserOrganization, Document, Spending, Contact, \
    SubPSGAllocation
from django.forms.models import BaseModelFormSet
from django.forms.models import inlineformset_factory


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['rows'] = '3'
        self.fields['startDate'].widget.attrs['class'] = 'form-control'
        self.fields['endDate'].widget.attrs['class'] = 'form-control'
        self.fields['funders'].widget.attrs['class'] = 'form-control'
        self.fields['implementers'].widget.attrs['class'] = 'form-control'
        self.fields['value'].widget.attrs['class'] = 'form-control'
        self.fields['currency'].widget.attrs['class'] = 'form-control'
        self.fields['rateToUSD'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Project
        exclude = ('id', 'lastModified', 'user', 'active')


class BaseLocationAllocationFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseLocationAllocationFormSet, self).__init__(*args, **kwargs)
        self.queryset = LocationAllocation.objects.none()


class BaseSubPSGAllocationFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseSubPSGAllocationFormSet, self).__init__(*args, **kwargs)
        self.queryset = SubPSGAllocation.objects.none()


class BaseSectorAllocationFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseLocationAllocationFormSet, self).__init__(*args, **kwargs)
        self.queryset = SectorAllocation.objects.none()


class BaseDocumentFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseDocumentFormSet, self).__init__(*args, **kwargs)
        self.queryset = Document.objects.none()


class BaseUserOrganizationFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseUserOrganizationFormSet, self).__init__(*args, **kwargs)
        self.queryset = UserOrganization.objects.none()


class BaseContactFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseContactFormSet, self).__init__(*args, **kwargs)
        self.queryset = Contact.objects.none()


class SectorAllocationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SectorAllocationForm, self).__init__(*args, **kwargs)
        self.fields['sector'].widget.attrs['class'] = 'form-control'
        self.fields['allocatedPercentage'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = SectorAllocation
        exclude = ('id', 'project')


class LocationAllocationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationAllocationForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs['class'] = 'form-control'
        self.fields['sublocations'].widget.attrs['class'] = 'form-control'
        self.fields['allocatedPercentage'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = LocationAllocation
        exclude = ('id', 'project')


class SubPSGAllocationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubPSGAllocationForm, self).__init__(*args, **kwargs)
        self.fields['psg'].widget.attrs['class'] = 'form-control'
        self.fields['subpsg'].widget.attrs['class'] = 'form-control'
        self.fields['allocatedPercentage'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = SubPSGAllocation
        exclude = ('id', 'project')


class UserOrganizationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserOrganizationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['role'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserOrganization
        exclude = ('id', 'project')


class DocumentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Document
        exclude = ('project', 'id')


class SpendingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpendingForm, self).__init__(*args, **kwargs)
        self.fields['spendingToDate'].widget.attrs['class'] = 'form-control'
        self.fields['nextYearSpending'].widget.attrs['class'] = 'form-control'
        self.fields['lastYearSpending'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Spending
        exclude = ('project',)


class ContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['organization'].widget.attrs['class'] = 'form-control'
        self.fields['number'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Contact
        exclude = ('project',)


LocationAllocationFormset = inlineformset_factory(Project, LocationAllocation, fields=('location', 'sublocations',
                                                                                       'allocatedPercentage'),
                                                  can_delete=True, extra=1, form=LocationAllocationForm)

SubPSGAllocationFormset = inlineformset_factory(Project, SubPSGAllocation, fields=('psg', 'subpsg',
                                                                                   'allocatedPercentage'),
                                                can_delete=True, extra=1, form=SubPSGAllocationForm)

SectorAllocationFormset = inlineformset_factory(Project, SectorAllocation, fields=('sector', 'allocatedPercentage'),
                                                can_delete=True, extra=1, form=SectorAllocationForm)

UserOrganizationFormset = inlineformset_factory(Project, UserOrganization, fields=('name', 'role'),
                                                can_delete=True, extra=1, form=UserOrganizationForm)

DocumentFormset = inlineformset_factory(Project, Document, fields=('name', 'file'), can_delete=True, extra=1,
                                        form=DocumentForm)
