from django.contrib import admin
from .models import Organization, Location, SubLocation, Sector, Currency, ExchangeRate, PSG, SubPSG


class SubLocationInline(admin.TabularInline):
    model = SubLocation
    extra = 1


class LocationAdmin(admin.ModelAdmin):
    inlines = [SubLocationInline]


class SubPSGInline(admin.TabularInline):
    model = SubPSG
    extra = 1


class PSGAdmin(admin.ModelAdmin):
    inlines = [SubPSGInline]


class ExchangeRateModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True

admin.site.register(Organization)
admin.site.register(Location, LocationAdmin)
admin.site.register(ExchangeRate, ExchangeRateModelAdmin)
admin.site.register(SubLocation)
admin.site.register(Sector)
admin.site.register(Currency)
admin.site.register(PSG, PSGAdmin)
admin.site.register(SubPSG)
