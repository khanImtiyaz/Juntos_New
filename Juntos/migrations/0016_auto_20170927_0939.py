# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-27 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0015_auto_20170927_0916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productsmanagement',
            old_name='product_image',
            new_name='image',
        ),
    ]
