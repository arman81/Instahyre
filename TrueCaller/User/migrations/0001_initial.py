# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-24 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=256)),
                ('phonenumber', models.IntegerField()),
                ('deviceId', models.CharField(max_length=100)),
            ],
        ),
    ]
