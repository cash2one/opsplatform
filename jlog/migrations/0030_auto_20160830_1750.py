# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-30 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jlog', '0029_auto_20160829_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termlog',
            name='timestamp',
            field=models.IntegerField(default=1472550648),
        ),
    ]
