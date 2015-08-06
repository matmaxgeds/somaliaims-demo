# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_entry', '0007_project_website'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='website',
        ),
        migrations.AddField(
            model_name='document',
            name='link_to_document_website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='/Users/alphabuddha/Projects/somaliaims/somaliaims/documents', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
