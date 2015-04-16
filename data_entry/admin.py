from django.contrib import admin
from management.models import Location, SubLocation
from .models import Project, ExchangeRate, LocationAllocation, SectorAllocation, Spending, Contact, Document, \
    UserOrganization


class ExchangerateModelAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True


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
    filter_horizontal = ( 'locations',  'sublocations', 'funders', 'implementers')
    inlines = [
            UserOrnanizationInline, LocationShareInline, SectorShareInline, SpendingInline
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(UserOrganization)
admin.site.register(ExchangeRate, ExchangerateModelAdmin)
admin.site.register(LocationAllocation)
admin.site.register(SectorAllocation)
admin.site.register(Contact)
admin.site.register(Spending)
admin.site.register(Document)
