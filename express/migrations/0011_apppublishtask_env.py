# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-15 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0010_auto_20160811_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='apppublishtask',
            name='env',
            field=models.CharField(default=1, max_length=50, verbose_name='\u73af\u5883\u7c7b\u578b'),
            preserve_default=False,
        ),
    ]
