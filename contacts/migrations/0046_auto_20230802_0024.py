# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2023-08-02 06:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0045_auto_20230802_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='agree',
            field=models.BooleanField(choices=[(True, 'I Accept The Minimums Outlined By Colorado Wealth Group In Their Fee Structure.*')], default=False),
        ),
    ]
