# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-04 15:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0022_auto_20161104_1525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publishtaskdeploy',
            old_name='publishtask',
            new_name='publish_task',
        ),
    ]