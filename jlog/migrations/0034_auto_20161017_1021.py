# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-17 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jlog', '0033_auto_20160927_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termlog',
            name='timestamp',
            field=models.IntegerField(default=1476670903),
        ),
    ]
