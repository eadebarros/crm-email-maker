# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('html_builder', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='structure',
            old_name='code',
            new_name='code_1',
        ),
        migrations.AddField(
            model_name='structure',
            name='code_2',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='structure',
            name='code_3',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='structure',
            name='code_4',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='structure',
            name='code_5',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='structure',
            name='code_6',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
