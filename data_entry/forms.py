from django.forms import ModelForm
from .models import Project, LocationAllocation, SectorAllocation, UserOrganization, Document, Spending, Contact
from django.forms.models import BaseModelFormSet
from django.forms.models import inlineformset_factory


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('id', 'lastModified', 'user', 'active')


class BaseLocationAllocationFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseLocationAllocationFormSet, self).__init__(*args, **kwargs)
        self.queryset = LocationAllocation.objects.none()


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
    class Meta:
        model = SectorAllocation
        exclude = ('id', 'project')


class LocationAllocationForm(ModelForm):
    class Meta:
        model = LocationAllocation
        exclude = ('id', 'project')


class UserOrganizationForm(ModelForm):
    class Meta:
        model = UserOrganization
        exclude = ('id', 'project')


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        exclude = ('project', 'id')


class SpendingForm(ModelForm):
    class Meta:
        model = Spending
        exclude = ('project',)


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        exclude = ('project',)


LocationAllocationFormset = inlineformset_factory(Project, LocationAllocation, fields=('location', 'sublocations',
                                                                                       'allocatedPercentage'),
                                                  can_delete=True, extra=1)

SectorAllocationFormset = inlineformset_factory(Project, SectorAllocation, fields=('sector', 'allocatedPercentage'),
                                                can_delete=True, extra=1)

UserOrganizationFormset = inlineformset_factory(Project, UserOrganization, fields=('name', 'role'),
                                                can_delete=True, extra=1)

DocumentFormset = inlineformset_factory(Project, Document, fields=('name', 'file'), can_delete=True, extra=1)

