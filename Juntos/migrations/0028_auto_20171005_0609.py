# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-05 06:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0027_auto_20171004_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billing_first_name', models.CharField(default='', max_length=50, verbose_name='Billing First Name')),
                ('billing_last_name', models.CharField(default='', max_length=50, verbose_name='Billing Last Name')),
                ('billing_company', models.CharField(default='', max_length=50, verbose_name='Billing Company')),
                ('billing_country', models.CharField(default='', max_length=50, verbose_name='Billing Country')),
                ('billing_country_abbreviation', models.CharField(default='', max_length=50, verbose_name='Billing Country Abbreviation')),
                ('billing_state', models.CharField(default='', max_length=50, verbose_name='Billing State')),
                ('billing_city', models.CharField(default='', max_length=50, verbose_name='Billing City')),
                ('billing_zip', models.CharField(default='', max_length=50, verbose_name='Billing Zip')),
                ('billing_address', models.CharField(default='', max_length=50, verbose_name='Billing Address')),
                ('billing_email', models.CharField(default='', max_length=50, verbose_name='Billing Email')),
                ('mode_of_transport', models.CharField(blank=True, default='', max_length=50, verbose_name='Mode of Transport')),
                ('selected', models.BooleanField(default=False, verbose_name='Select Shipping Address')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='billing_address',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='billing_city',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='billing_company',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='billing_country',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='billing_country_abbreviation',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='billing_email',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='billing_first_name',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='billing_last_name',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='billing_state',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='billing_zip',
        ),
    ]
