# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('html_builder', '0002_auto_20151110_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='filter',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='structure',
            name='tile',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
