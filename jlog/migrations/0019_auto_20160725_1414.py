# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jlog', '0018_auto_20160719_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termlog',
            name='timestamp',
            field=models.IntegerField(default=1469427273),
        ),
    ]
