# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-30 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0012_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=100, verbose_name='\u9879\u76ee\u540d\u79f0'),
        ),
    ]