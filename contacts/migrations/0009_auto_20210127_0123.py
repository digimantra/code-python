# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2021-01-27 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_auto_20210127_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='household_income',
            field=models.CharField(choices=[('Blank', ''), ('<$100K', '<$100K'), ('$101-250k', '$101-250k'), ('$250-500k', '$250-500k'), ('$500-1mm', '$500-1mm'), ('$1-2mm', '$1-2mm'), ('$2mm+', '$2mm+')], default='Blank', max_length=255, verbose_name='household income'),
        ),
        migrations.AlterField(
            model_name='message',
            name='investeble_assets',
            field=models.CharField(choices=[('Blank', ''), ('<$100K', '<$100K'), ('$101-250k', '$101-250k'), ('$250-500k', '$250-500k'), ('$500-1mm', '$500-1mm'), ('$1-2mm', '$1-2mm'), ('$2mm+', '$2mm+')], default='Blank', max_length=255, verbose_name='investeble assets'),
        ),
        migrations.AlterField(
            model_name='message',
            name='marital_status',
            field=models.CharField(choices=[('Blank', ''), ('Married', 'Married'), ('Not Married', 'Not Married')], default='Blank', max_length=255, verbose_name='marital status'),
        ),
        migrations.AlterField(
            model_name='message',
            name='number_of_children',
            field=models.CharField(choices=[('Blank', ''), ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='Blank', max_length=255, verbose_name='number of children'),
        ),
    ]