# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='lastModified',
            field=models.DateField(null=True, auto_now=True),
        ),
    ]
