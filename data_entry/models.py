from management.models import Organization, Currency, Location, Sector, SubLocation
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import datetime
import uuid


class UnsavedForeighKey(models.ForeignKey):
    allow_unsaved_instance_assignment = True


class Project(models.Model):
    """Projects receiving AID"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=250)
    description = models.TextField()
    lastModified = models.DateField(blank=True, null=True)
    startDate = models.DateField()
    endDate = models.DateField()
    funders = models.ManyToManyField(Organization, related_name="funders")
    implementers = models.ManyToManyField(Organization, related_name="implementers")
    value = models.FloatField()
    currency = models.ForeignKey(Currency)
    rateToUSD = models.DecimalField(max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True, blank=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.name

    def save(self):
        if datetime.date.today() > self.endDate:
            self.active = False
        if self.id:
            self.lastModified = datetime.datetime.now()
        else:
            pass
        super(Project, self).save()


class Spending(models.Model):
    """How a project's value has and is intended to been spent"""
    project = models.OneToOneField(Project)
    spendingToDate = models.FloatField(help_text="Total amount of aid spent up to date")
    lastYearSpending = models.FloatField(help_text="Total amount of aid spent last year")
    nextYearSpending = models.FloatField(help_text="Total amount of aid anticipated to be spent next year")

    class Meta:
        db_table = 'project_spending'

    def __str__(self):
        return self.project.name


class Contact(models.Model):
    """Person who knows more about the Project"""
    project = models.OneToOneField(Project)
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        db_table = 'project_contacts'

    def __str__(self):
        return self.name


class Document(models.Model):
    """Documents relevant to a project"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = UnsavedForeighKey(Project)
    file = models.FileField(upload_to=settings.DOCUMENT_UPLOAD_DIR)
    name = models.CharField(max_length=150)

    class Meta:
        db_table = 'project_documents'

    def __str__(self):
        return "{0}".format(self.name)


class SectorAllocation(models.Model):
    """Amount of project's value spent in various sectors"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = UnsavedForeighKey(Project)
    sector = models.ForeignKey(Sector)
    allocatedPercentage = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        db_table = 'sector_allocations'

    def __str__(self):
        return "{0} - {1} - {2}".format(self.project.name, self.sector.name, self.allocatedPercentage)


class LocationAllocation(models.Model):
    """Amount of project's value spent in various locations"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = UnsavedForeighKey(Project)
    location = models.ForeignKey(Location)
    sublocations = models.ManyToManyField(SubLocation)
    allocatedPercentage = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        db_table = 'location_allocations'

    def __str__(self):
        return "{0} - {1} - {2}".format(self.project.name, self.location.name, self.allocatedPercentage)


class UserOrganization(models.Model):
    """Organizations missing in organization list but involved in projects. User defined"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    project = UnsavedForeighKey(Project)
    name = models.CharField(max_length=200,  help_text="Organization involved in project but not in existing list",
                            unique=True)
    role = models.CharField(max_length=12, choices=(('Funder', 'Funder'), ('Implementer', 'Implementer')),
                            help_text="Role of organization in project")

    class Meta:
        db_table = 'user_organisations'

    def __str__(self):
        return self.name