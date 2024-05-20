# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2023-11-23 06:15
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0047_auto_20231107_0444'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleSubscribePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', libs.stdimage.fields.StdImageField(aspects='normal', blank=True, min_dimensions=(1200, 1200), upload_to='page', variations={'admin': {'size': (200, 150)}, 'desktop': {'size': (1470, 510)}, 'mobile': {'size': (640, 380)}, 'mobile_2x': {'quality': 80, 'size': (1280, 760)}, 'tablet': {'size': (767, 400)}, 'tablet_2x': {'quality': 80, 'size': (1534, 800)}, 'wide': {'size': (1920, 660)}}, verbose_name='image')),
                ('header', models.CharField(max_length=255, verbose_name='header')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('text_first', ckeditor.fields.CKEditorUploadField(blank=True, help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', verbose_name='first text')),
                ('text_second', ckeditor.fields.CKEditorUploadField(blank=True, help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', verbose_name='second text')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'Subscribe',
            },
        ),
    ]
