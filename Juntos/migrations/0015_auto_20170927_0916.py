# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-27 09:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0014_auto_20170927_0844'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productsmanagement',
            old_name='image',
            new_name='product_image',
        ),
    ]
