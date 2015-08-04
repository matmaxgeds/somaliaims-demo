# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0004_subpsgallocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='spending',
            name='thisYearSpending',
            field=models.FloatField(help_text='Amount expected to be spent this year', default=1000000, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='spending',
            name='lastYearSpending',
            field=models.FloatField(null=True, help_text='Total amount of aid spent last year', blank=True),
        ),
        migrations.AlterField(
            model_name='spending',
            name='nextYearSpending',
            field=models.FloatField(null=True, help_text='Total amount of aid anticipated to be spent next year', blank=True),
        ),
        migrations.AlterField(
            model_name='spending',
            name='spendingToDate',
            field=models.FloatField(null=True, help_text='Total amount of aid spent up to date', blank=True),
        ),
    ]
