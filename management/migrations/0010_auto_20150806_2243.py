# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_auto_20150806_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='short_name',
            field=models.CharField(null=True, max_length=200, blank=True),
        ),
    ]
