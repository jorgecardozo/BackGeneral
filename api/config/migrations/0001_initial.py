# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-14 09:56
from __future__ import unicode_literals

from django.db import migrations, models

def InitialData(apps, schema_editor):
    DefaultConfig = apps.get_model('config', 'DefaultConfig')
    default = DefaultConfig()
    default.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decimalesCant', models.IntegerField(default=2)),
                ('decimalesChar', models.CharField(max_length=1)),
                ('milesChar', models.CharField(max_length=1)),
            ],
        ),
        migrations.RunPython(InitialData)
    ]
