# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-28 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0017_auto_20170928_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsmanagement',
            name='payment_mode',
            field=models.CharField(choices=[['All', 'All'], ['COD', 'Cash on Delivery'], ['Online', 'Online Payment'], ['Paypal', 'Paypal']], default='All', max_length=10, verbose_name='Payment Mode'),
        ),
    ]
