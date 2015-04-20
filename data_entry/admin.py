from django.contrib import admin
from .models import Project, LocationAllocation, SectorAllocation, Spending, Contact, Document, \
    UserOrganization


class UserOrnanizationInline(admin.TabularInline):
    model = UserOrganization
    extra = 1


class LocationShareInline(admin.TabularInline):
    model = LocationAllocation
    extra = 1


class SectorShareInline(admin.TabularInline):
    model = SectorAllocation
    extra = 1


class SpendingInline(admin.TabularInline):
    model = Spending


class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('locations',  'sublocations', 'funders', 'implementers', 'sectors')
    inlines = [
            UserOrnanizationInline, LocationShareInline, SectorShareInline, SpendingInline
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(UserOrganization)
admin.site.register(LocationAllocation)
admin.site.register(SectorAllocation)
admin.site.register(Contact)
admin.site.register(Spending)
admin.site.register(Document)
