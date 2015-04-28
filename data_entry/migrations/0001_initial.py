# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import data_entry.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'db_table': 'project_contacts',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False)),
                ('file', models.FileField(upload_to='/home/kevin/code/django/somaliaims/documents')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'project_documents',
            },
        ),
        migrations.CreateModel(
            name='LocationAllocation',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False)),
                ('allocatedPercentage', models.DecimalField(decimal_places=1, max_digits=4)),
                ('location', models.ForeignKey(to='management.Location')),
            ],
            options={
                'db_table': 'location_allocations',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('lastModified', models.DateField(blank=True, null=True)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('value', models.FloatField()),
                ('rateToUSD', models.DecimalField(decimal_places=4, max_digits=4)),
                ('active', models.BooleanField(default=True)),
                ('currency', models.ForeignKey(to='management.Currency')),
                ('funders', models.ManyToManyField(to='management.Organization', related_name='funders')),
                ('implementers', models.ManyToManyField(to='management.Organization', related_name='implementers')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='SectorAllocation',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False)),
                ('allocatedPercentage', models.DecimalField(decimal_places=1, max_digits=4)),
                ('project', data_entry.models.UnsavedForeighKey(to='data_entry.Project')),
                ('sector', models.ForeignKey(to='management.Sector')),
            ],
            options={
                'db_table': 'sector_allocations',
            },
        ),
        migrations.CreateModel(
            name='Spending',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('spendingToDate', models.FloatField(help_text='Total amount of aid spent up to date')),
                ('lastYearSpending', models.FloatField(help_text='Total amount of aid spent last year')),
                ('nextYearSpending', models.FloatField(help_text='Total amount of aid anticipated to be spent next year')),
                ('project', models.OneToOneField(to='data_entry.Project')),
            ],
            options={
                'db_table': 'project_spending',
            },
        ),
        migrations.CreateModel(
            name='UserOrganization',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False)),
                ('name', models.CharField(max_length=200, unique=True, help_text='Organization involved in project but not in existing list')),
                ('role', models.CharField(max_length=12, choices=[('Funder', 'Funder'), ('Implementer', 'Implementer')], help_text='Role of organization in project')),
                ('project', data_entry.models.UnsavedForeighKey(to='data_entry.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_organisations',
            },
        ),
        migrations.AddField(
            model_name='locationallocation',
            name='project',
            field=data_entry.models.UnsavedForeighKey(to='data_entry.Project'),
        ),
        migrations.AddField(
            model_name='locationallocation',
            name='sublocations',
            field=models.ManyToManyField(to='management.SubLocation'),
        ),
        migrations.AddField(
            model_name='document',
            name='project',
            field=data_entry.models.UnsavedForeighKey(to='data_entry.Project'),
        ),
        migrations.AddField(
            model_name='contact',
            name='project',
            field=models.OneToOneField(to='data_entry.Project'),
        ),
    ]
