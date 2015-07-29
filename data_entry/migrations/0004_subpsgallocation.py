# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import data_entry.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_psg_subpsg'),
        ('data_entry', '0003_auto_20150728_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubPSGAllocation',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4, editable=False)),
                ('allocatedPercentage', models.DecimalField(max_digits=4, decimal_places=1)),
                ('project', data_entry.models.UnsavedForeighKey(to='data_entry.Project')),
                ('psg', models.ForeignKey(to='management.PSG')),
                ('subpsg', models.ForeignKey(to='management.SubPSG')),
            ],
            options={
                'db_table': 'subpsg_allocations',
            },
        ),
    ]
