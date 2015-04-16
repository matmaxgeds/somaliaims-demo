from django.contrib import admin
from .models import Organization, Location, SubLocation, Sector, Currency


class SubLocationInline(admin.TabularInline):
    model = SubLocation
    extra = 1

class LocationAdmin(admin.ModelAdmin):
    inlines = [SubLocationInline]

admin.site.register(Organization)
admin.site.register(Location, LocationAdmin)
admin.site.register(SubLocation)
admin.site.register(Sector)
admin.site.register(Currency)
