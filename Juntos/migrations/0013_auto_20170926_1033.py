# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-26 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0012_auto_20170926_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsmanagement',
            name='expire_products',
            field=models.IntegerField(blank=True, default=15, null=True, verbose_name='Expired Products'),
        ),
    ]
