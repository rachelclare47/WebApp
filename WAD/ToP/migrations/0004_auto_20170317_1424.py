# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-17 14:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ToP', '0003_auto_20170307_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
