# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import management.models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_auto_20150806_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subpsg',
            name='psg',
            field=management.models.UnsavedForeighKey(to='management.PSG'),
        ),
    ]
