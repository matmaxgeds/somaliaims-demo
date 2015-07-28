# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20150520_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='PSG',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'psg',
            },
        ),
        migrations.CreateModel(
            name='SubPSG',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('psg', models.ForeignKey(to='management.PSG')),
            ],
            options={
                'verbose_name_plural': 'sub-psgs',
                'db_table': 'sub_psg',
            },
        ),
    ]
