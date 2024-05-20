# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2021-02-11 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0025_auto_20210209_0459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='additional_information',
            field=models.CharField(blank=True, max_length=1024, verbose_name='additional information*'),
        ),
        migrations.AlterField(
            model_name='message',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Full name*'),
        ),
        migrations.AlterField(
            model_name='message',
            name='number_of_children',
            field=models.CharField(choices=[('', ''), ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5+', '5+')], default='', max_length=255, verbose_name='number of children*'),
        ),
        migrations.AlterField(
            model_name='message',
            name='occupation',
            field=models.CharField(blank=True, max_length=255, verbose_name='occupation*'),
        ),
    ]
