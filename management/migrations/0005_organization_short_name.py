# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_psg_subpsg'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='short_name',
            field=models.CharField(null=True, max_length=20, blank=True),
        ),
    ]
