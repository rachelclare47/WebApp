# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-03-18 17:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ToP', '0005_auto_20170317_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime(2017, 3, 18, 17, 26, 54, 817000))),
                ('approved_comment', models.BooleanField(default=False)),
                ('playlists', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ToP.Playlist')),
            ],
        ),
    ]