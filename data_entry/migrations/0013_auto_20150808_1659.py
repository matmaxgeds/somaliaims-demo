# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0012_auto_20150807_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='organization',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
