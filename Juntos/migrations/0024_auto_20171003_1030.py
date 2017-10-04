# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-03 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0023_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsmanagement',
            name='product_quantity',
            field=models.IntegerField(default=0, verbose_name='Product Available Quantity'),
        ),
        migrations.AlterField(
            model_name='productsmanagement',
            name='product_rating',
            field=models.IntegerField(blank=True, default=0, verbose_name='Product Rating'),
        ),
    ]
