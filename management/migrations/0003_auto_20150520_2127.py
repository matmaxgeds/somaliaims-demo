# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20150520_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='lng',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='sublocation',
            name='lat',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='sublocation',
            name='lng',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
