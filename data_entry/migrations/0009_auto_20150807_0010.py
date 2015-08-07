# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0008_auto_20150805_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='endDate',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='startDate',
            field=models.DateField(null=True, blank=True),
        ),
    ]
