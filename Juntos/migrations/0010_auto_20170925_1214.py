# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-25 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0009_auto_20170925_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='vendor_step',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Vendor Step'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='confirmation_code',
            field=models.CharField(default='Not Confirmed', max_length=50, verbose_name='confirmation_code'),
        ),
    ]
