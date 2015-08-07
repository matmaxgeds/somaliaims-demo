# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_auto_20150806_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='short_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
