# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2021-02-12 06:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0026_auto_20210211_0406'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Full name*')),
                ('phone', models.CharField(blank=True, max_length=32, verbose_name='phone')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='e-mail')),
                ('message', models.TextField(max_length=2048, verbose_name='message')),
                ('additional_information', models.CharField(blank=True, max_length=1024, verbose_name='additional information')),
                ('referer', models.CharField(blank=True, editable=False, max_length=512, verbose_name='from page')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='date sent')),
            ],
            options={
                'verbose_name': 'Defaul message',
                'verbose_name_plural': 'Default messages',
                'ordering': ('-date',),
                'default_permissions': ('delete',),
            },
        ),
        migrations.DeleteModel(
            name='DefaultForm',
        ),
    ]