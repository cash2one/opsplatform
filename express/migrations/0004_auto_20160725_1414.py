# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 14:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0003_auto_20160719_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publishtask',
            name='type',
        ),
        migrations.AddField(
            model_name='publishtask',
            name='code_tag',
            field=models.CharField(max_length=100, null=True, verbose_name='Tag'),
        ),
        migrations.AddField(
            model_name='publishtask',
            name='create_by',
            field=models.CharField(default='', max_length=100, verbose_name='\u521b\u5efa\u4eba'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publishtask',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 25, 14, 14, 53, 774528), verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publishtask',
            name='database_update',
            field=models.TextField(null=True, verbose_name='\u6570\u636e\u5e93\u66f4\u65b0\u8bf4\u660e'),
        ),
        migrations.AddField(
            model_name='publishtask',
            name='env',
            field=models.CharField(default=1, max_length=50, verbose_name='\u73af\u5883\u7c7b\u578b'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publishtask',
            name='publish_time',
            field=models.DateTimeField(null=True, verbose_name='\u8ba1\u5212\u53d1\u7248\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='publishtask',
            name='upload_sql',
            field=models.CharField(max_length=1000, null=True, verbose_name='\u66f4\u65b0SQL\u6587\u4ef6'),
        ),
        migrations.AlterField(
            model_name='publishtask',
            name='code_dir',
            field=models.TextField(null=True, verbose_name='\u4ee3\u7801\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='publishtask',
            name='product',
            field=models.CharField(max_length=100, null=True, verbose_name='\u4ea7\u54c1\u7ebf'),
        ),
        migrations.AlterField(
            model_name='publishtask',
            name='settings',
            field=models.TextField(null=True, verbose_name='\u73af\u5883\u8bbe\u7f6e'),
        ),
        migrations.AlterField(
            model_name='publishtask',
            name='submit_by',
            field=models.CharField(max_length=100, null=True, verbose_name='\u63d0\u4ea4\u4eba'),
        ),
        migrations.AlterField(
            model_name='publishtask',
            name='submit_time',
            field=models.DateTimeField(null=True, verbose_name='\u63d0\u4ea4\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='publishtask',
            name='update_note',
            field=models.TextField(null=True, verbose_name='\u66f4\u65b0\u8bf4\u660e'),
        ),
    ]