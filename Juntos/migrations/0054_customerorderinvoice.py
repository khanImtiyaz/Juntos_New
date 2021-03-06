# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-23 10:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0053_taxpercentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerOrderInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(blank=True, max_length=100, verbose_name='Invoice Number')),
                ('shipping_charge', models.FloatField(blank=True, null=True, verbose_name='Shipping charge')),
                ('shippment_date', models.DateField(blank=True, null=True, verbose_name='Shippment Date')),
                ('billing_info', models.TextField(blank=True, verbose_name='Billing Information')),
                ('shipping_info', models.TextField(blank=True, verbose_name='Shipping Information')),
                ('ready_by_time', models.CharField(blank=True, max_length=10, verbose_name='Ready by Time')),
                ('close_time', models.CharField(blank=True, max_length=10, verbose_name='Close Time')),
                ('pickup_date', models.DateField(blank=True, null=True, verbose_name='Pickup Date')),
                ('payment_method', models.CharField(blank=True, max_length=100, verbose_name='Payment Method')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('item_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemOrderInvoice', to='Juntos.OrderItems')),
            ],
        ),
    ]
