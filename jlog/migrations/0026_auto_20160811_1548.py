# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-11 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jlog', '0025_auto_20160808_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termlog',
            name='timestamp',
            field=models.IntegerField(default=1470901719),
        ),
    ]
