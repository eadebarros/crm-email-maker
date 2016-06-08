# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id_html_builder_main', models.AutoField(serialize=False, primary_key=True)),
                ('campaign', models.CharField(default=None, max_length=500, null=True)),
                ('category', models.CharField(default=None, max_length=500, null=True)),
                ('country', models.CharField(default=None, max_length=2, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id_html_builder_structure', models.AutoField(serialize=False, primary_key=True)),
                ('fk_html_builder_main', models.IntegerField(null=True)),
                ('name', models.CharField(default=None, max_length=500, null=True)),
                ('url_img_1', models.CharField(default=None, max_length=1000, null=True)),
                ('url_img_mobile_1', models.CharField(max_length=1000, null=True)),
                ('url_link_1', models.CharField(max_length=1000, null=True)),
                ('url_deeplink_1', models.CharField(max_length=1000, null=True)),
                ('alt_title_1', models.CharField(max_length=1000, null=True)),
                ('url_img_2', models.CharField(default=None, max_length=1000, null=True)),
                ('url_link_2', models.CharField(max_length=1000, null=True)),
                ('url_deeplink_2', models.CharField(max_length=1000, null=True)),
                ('alt_title_2', models.CharField(max_length=1000, null=True)),
                ('url_img_3', models.CharField(default=None, max_length=1000, null=True)),
                ('url_link_3', models.CharField(max_length=1000, null=True)),
                ('url_deeplink_3', models.CharField(max_length=1000, null=True)),
                ('alt_title_3', models.CharField(max_length=1000, null=True)),
                ('url_img_4', models.CharField(default=None, max_length=1000, null=True)),
                ('url_link_4', models.CharField(max_length=1000, null=True)),
                ('url_deeplink_4', models.CharField(max_length=1000, null=True)),
                ('alt_title_4', models.CharField(max_length=1000, null=True)),
                ('url_img_5', models.CharField(default=None, max_length=1000, null=True)),
                ('url_link_5', models.CharField(max_length=1000, null=True)),
                ('url_deeplink_5', models.CharField(max_length=1000, null=True)),
                ('alt_title_5', models.CharField(max_length=1000, null=True)),
                ('url_img_6', models.CharField(default=None, max_length=1000, null=True)),
                ('url_link_6', models.CharField(max_length=1000, null=True)),
                ('url_deeplink_6', models.CharField(max_length=1000, null=True)),
                ('alt_title_6', models.CharField(max_length=1000, null=True)),
                ('is_deeplink', models.CharField(max_length=500, null=True)),
                ('code', models.CharField(max_length=500, null=True)),
                ('order', models.CharField(max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
