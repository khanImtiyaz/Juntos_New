# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-14 12:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0040_advertisementimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisementimage',
            name='advertisement_images',
        ),
        migrations.DeleteModel(
            name='AdvertisementImage',
        ),
    ]
