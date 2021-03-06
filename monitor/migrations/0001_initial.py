# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-27 10:01
from __future__ import unicode_literals

from django.db import migrations, models
import opsplatform.until


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TmpGraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', opsplatform.until.UnixTimestampField(auto_created=True, db_column=b'time_', null=True)),
                ('endpoints', models.CharField(default=b'', max_length=10240, verbose_name=b'Endpoint')),
                ('counters', models.CharField(default=b'', max_length=10240, verbose_name=b'Counters')),
                ('ck', models.CharField(max_length=32, verbose_name=b'ck')),
            ],
        ),
    ]
