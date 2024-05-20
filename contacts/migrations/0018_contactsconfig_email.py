# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2021-01-29 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0017_auto_20210129_0516'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactsconfig',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='e-mail'),
            preserve_default=False,
        ),
    ]
