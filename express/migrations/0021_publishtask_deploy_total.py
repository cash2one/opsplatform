# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-25 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0020_auto_20161024_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishtask',
            name='deploy_total',
            field=models.CharField(max_length=100, null=True, verbose_name='\u53d1\u5e03\u6240\u9700\u6b65\u9aa4'),
        ),
    ]
