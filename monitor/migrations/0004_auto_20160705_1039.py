# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_dashboardscreenheart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardgraph',
            name='counters',
            field=models.CharField(max_length=10240, verbose_name=b'counters'),
        ),
        migrations.AlterField(
            model_name='dashboardgraph',
            name='hosts',
            field=models.CharField(max_length=10240, verbose_name=b'hosts'),
        ),
        migrations.AlterField(
            model_name='dashboardgraph',
            name='screen_id',
            field=models.CharField(max_length=1000, verbose_name=b'screen_id'),
        ),
    ]
