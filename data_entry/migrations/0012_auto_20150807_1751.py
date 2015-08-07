# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0011_auto_20150807_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.TextField(),
        ),
    ]
