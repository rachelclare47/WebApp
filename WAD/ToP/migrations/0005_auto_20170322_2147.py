# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-03-22 21:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToP', '0004_auto_20170322_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')], default=1),
        ),
    ]
