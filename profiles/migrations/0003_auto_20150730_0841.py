# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0005_auto_20150729_1513'),
        ('profiles', '0002_auto_20150729_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='organization2',
            field=models.ForeignKey(null=True, to='data_entry.UserOrganization', blank=True, verbose_name="If the user's organizations is in the additional organizations list"),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='organization',
            field=models.ForeignKey(null=True, to='management.Organization', blank=True),
        ),
    ]
