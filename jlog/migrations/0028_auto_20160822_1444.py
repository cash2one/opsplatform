# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-22 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jlog', '0027_auto_20160815_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termlog',
            name='timestamp',
            field=models.IntegerField(default=1471848286),
        ),
    ]
