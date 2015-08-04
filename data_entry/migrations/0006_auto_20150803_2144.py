# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0005_auto_20150729_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='capacity_building',
            field=models.CharField(max_length=20, choices=[(None, ' '), ('Principal', 'Principal'), ('Significant', 'Significant'), ('Not targeted', 'Not targeted'), ('NA', 'NA')], null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='conflict_sensitivity_analysis',
            field=models.CharField(max_length=100, choices=[(None, ' '), ('Conflict analysis conducted and updated regularly', 'Conflict analysis conducted and updated regularly'), ('Conflict analysis conducted once but not updated', 'Conflict analysis conducted once but not updated'), ('No conflict analysis conducted for activity', 'No conflict analysis conducted for activity')], null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='conflict_sensitivity_monitoring',
            field=models.NullBooleanField(choices=[(None, ' '), (True, 'Yes'), (False, 'No')]),
        ),
        migrations.AddField(
            model_name='project',
            name='funding_channel',
            field=models.CharField(max_length=20, choices=[(None, ' '), ('Channel 1', 'Channel 1'), ('Channel 2', 'Channel 2'), ('Channel 3', 'Channel 3')], null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='funding_instrument',
            field=models.CharField(max_length=100, choices=[(None, ' '), ('General Budget Support', 'General Budget Support'), ('Sector Budget Support', 'Sector Budget Support'), ('Pooled fund', 'Pooled fund'), ('Project/program', 'Project/program')], null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='gender',
            field=models.CharField(max_length=20, choices=[(None, ' '), ('Principal', 'Principal'), ('Significant', 'Significant'), ('Not targeted', 'Not targeted'), ('NA', 'NA')], null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='ocha_fts_reported',
            field=models.NullBooleanField(choices=[(None, ' '), (True, 'Yes'), (False, 'No')]),
        ),
        migrations.AddField(
            model_name='project',
            name='sdrf_ssa',
            field=models.CharField(max_length=100, choices=[(None, ' '), ('WB Multi-Partner Fund (MPF)', 'WB Multi-Partner Fund (MPF)'), ('UN Multi-Partner Trust Fund (MPTF)', 'UN Multi-Partner Trust Fund (MPTF)'), ('African Development Bank Multi-Partner Programme (AMPP)', 'African Development Bank Multi-Partner Programme (AMPP)'), ('Special Financing Facility (SFF)', 'Special Financing Facility (SFF)'), ('Somalia Stability Fund (SSF)', 'Somalia Stability Fund (SSF)'), ('Not using SDRF', 'Not using SDRF')], null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='stabilization',
            field=models.CharField(max_length=20, choices=[(None, ' '), ('Principal', 'Principal'), ('Significant', 'Significant'), ('Not targeted', 'Not targeted'), ('NA', 'NA')], null=True, blank=True),
        ),
    ]
