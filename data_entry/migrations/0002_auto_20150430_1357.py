# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='/home/alphabuddha/Documents/somaliaims/somaliaims/documents'),
        ),
        migrations.AlterField(
            model_name='project',
            name='rateToUSD',
            field=models.DecimalField(max_digits=6, decimal_places=2),
        ),
    ]
