from django.db import models
from django.conf import settings
import uuid


class UnsavedForeighKey(models.ForeignKey):
    allow_unsaved_instance_assignment = True


class Organization(models.Model):
    """Organizations funding and implementing projects"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    short_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'organizations'

    def __str__(self):
        if self.short_name:
            return self.short_name
        else:
            return self.name


class Location(models.Model):
    """Regions within Somalia e.g Jubaland"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, unique=True)
    lng = models.CharField(max_length=50, blank=True)
    lat = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'locations'

    def __str__(self):
        return self.name


class SubLocation(models.Model):
    """Sub locations under Somalia's regions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = UnsavedForeighKey(Location)
    name = models.CharField(max_length=100, unique=False)
    lng = models.CharField(max_length=50, blank=True)
    lat = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'sublocations'

    def __str__(self):
        return "{0} - {1}".format(self.location.name, self.name)


class Sector(models.Model):
    """Sectors that are receiving funds from the projects"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    class Meta:
        db_table = 'sectors'

    def __str__(self):
        return self.name


class Currency(models.Model):
    """Currency abbreviations and their corresponding full names"""
    abbrev = models.CharField(max_length=settings.CURRENCY_ABBREVIATION_LENGTH, unique=True)
    currency = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Currencies"
        db_table = 'currencies'

    def __str__(self):
        return "{0}({1})".format(self.abbrev, self.currency)


class ExchangeRate(models.Model):
    """Universal conversion rate from USD to SOM. Set by manager."""
    dateSet = models.DateField(auto_now=True)
    rateToSOM = models.FloatField(default=0.00, blank=True, null=True)

    class Meta:
        db_table = 'exchange_rate_to_usd'

    def __str__(self):
        return str(self.rateToSOM)


class PSG(models.Model):
    """PSGs for projects"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'psg'

    def __str__(self):
        return self.name


class SubPSG(models.Model):
    """SubPSGs for projects"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    psg = models.ForeignKey(PSG)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'sub_psg'
        verbose_name_plural = 'sub-psgs'

    def __str__(self):
        return "{0} - {1}".format(self.psg, self.name)



