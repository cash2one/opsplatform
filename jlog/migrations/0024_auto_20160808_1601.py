# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jlog', '0023_auto_20160804_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termlog',
            name='timestamp',
            field=models.IntegerField(default=1470643266),
        ),
    ]