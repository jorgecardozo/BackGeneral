# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-23 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='accesosDirectos',
            field=models.TextField(blank=True, null=True),
        ),
    ]
