# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-15 14:02
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0044_paymentmethod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsmanagement',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='productsmanagement',
            name='feature',
            field=models.TextField(blank=True, default='Not a feature product', null=True, verbose_name='Features'),
        ),
        migrations.AlterField(
            model_name='productsmanagement',
            name='image',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(verbose_name='image'), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='productsmanagement',
            name='price',
            field=models.FloatField(verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='productsmanagement',
            name='product_quantity',
            field=models.IntegerField(default=0, verbose_name='Available Quantity'),
        ),
        migrations.AlterField(
            model_name='productsmanagement',
            name='product_rating',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='productsmanagement',
            name='product_sku',
            field=models.CharField(blank=True, max_length=50, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='productsmanagement',
            name='product_tag',
            field=models.CharField(blank=True, max_length=300, verbose_name='Tag'),
        ),
        migrations.AlterField(
            model_name='productsmanagement',
            name='selling_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Selling Price'),
        ),
        migrations.AlterField(
            model_name='productsmanagement',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Title'),
        ),
    ]