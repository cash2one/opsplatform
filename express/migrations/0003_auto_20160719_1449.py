# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0002_auto_20160719_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishtask',
            name='seq_no',
            field=models.CharField(max_length=50, verbose_name='\u53d1\u5e03\u5e8f\u5217\u53f7'),
        ),
    ]
