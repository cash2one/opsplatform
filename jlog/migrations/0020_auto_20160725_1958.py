# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jlog', '0019_auto_20160725_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termlog',
            name='timestamp',
            field=models.IntegerField(default=1469447884),
        ),
    ]
