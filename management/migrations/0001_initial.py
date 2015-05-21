# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import management.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('abbrev', models.CharField(max_length=3, unique=True)),
                ('currency', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
                'db_table': 'currencies',
            },
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('dateSet', models.DateField(auto_now=True)),
                ('rateToSOM', models.FloatField(null=True, blank=True, default=0.0)),
            ],
            options={
                'db_table': 'exchange_rate_to_usd',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('lat', models.CharField(max_length=12, blank=True)),
                ('long', models.CharField(max_length=12, blank=True)),
            ],
            options={
                'db_table': 'locations',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'organizations',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'sectors',
            },
        ),
        migrations.CreateModel(
            name='SubLocation',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('lat', models.CharField(max_length=12, blank=True)),
                ('long', models.CharField(max_length=12, blank=True)),
                ('location', management.models.UnsavedForeighKey(to='management.Location')),
            ],
            options={
                'db_table': 'sublocations',
            },
        ),
    ]
