# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2021-01-27 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0013_remove_message_spouse_date_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='spouse_date_birth',
            field=models.DateField(blank=True, null=True, verbose_name='spouse date birth'),
        ),
    ]