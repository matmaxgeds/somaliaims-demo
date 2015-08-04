from django.contrib import admin
from .models import Project, LocationAllocation, SectorAllocation, Spending, Contact, Document, \
    UserOrganization, SubPSGAllocation


class UserOrnanizationInline(admin.TabularInline):
    model = UserOrganization
    extra = 1


class LocationShareInline(admin.TabularInline):
    model = LocationAllocation
    extra = 1


class SubPSGShareInline(admin.TabularInline):
    model = SubPSGAllocation
    extra = 1


class SectorShareInline(admin.TabularInline):
    model = SectorAllocation
    extra = 1


class SpendingInline(admin.TabularInline):
    model = Spending


class ContactInline(admin.TabularInline):
    model = Contact


class DocumentInline(admin.TabularInline):
    model = Document


class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('funders', 'implementers')
    inlines = [
            UserOrnanizationInline, LocationShareInline, SectorShareInline, SubPSGShareInline, SpendingInline, ContactInline, DocumentInline
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(UserOrganization)
admin.site.register(LocationAllocation)
admin.site.register(SubPSGAllocation)
admin.site.register(SectorAllocation)
admin.site.register(Contact)
admin.site.register(Spending)
admin.site.register(Document)
