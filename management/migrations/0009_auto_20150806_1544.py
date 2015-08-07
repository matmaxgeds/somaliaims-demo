# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_auto_20150806_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psg',
            name='name',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='subpsg',
            name='name',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
