# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2023-07-31 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0043_auto_20230730_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Full name*'),
        ),
    ]
