# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_auto_20150806_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sector',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
