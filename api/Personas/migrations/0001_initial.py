# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-07 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Personas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('tipoDocumento', models.IntegerField()),
                ('documento', models.CharField(max_length=8)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]