# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-30 13:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0035_auto_20171023_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='Juntos.ProductsManagement'),
        ),
    ]
