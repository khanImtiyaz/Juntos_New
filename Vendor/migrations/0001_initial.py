# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-25 13:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Juntos', '0010_auto_20170925_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor_Account_Details',
            fields=[
                ('vendor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='account', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('legal_name', models.CharField(max_length=30, verbose_name='Legal name')),
                ('business_name', models.CharField(max_length=20, verbose_name='Business name')),
                ('business_url', models.CharField(blank=True, help_text='Ex: http://peru.com', max_length=50, null=True, verbose_name='Business Url')),
                ('agree_terms_condition', models.BooleanField(default=False, help_text='Clicking on this you are supposed to agree terms and condition of Peru Juntos', verbose_name='Agree Term & condition')),
                ('bank_name', models.CharField(max_length=30, verbose_name='Bank Name')),
                ('account_number', models.CharField(max_length=16, verbose_name='Account Number')),
                ('routing_number', models.CharField(max_length=20, verbose_name='Routing Number')),
                ('address1', models.TextField(default='', max_length=100, verbose_name='Address line 1')),
                ('address2', models.TextField(blank=True, default='', max_length=100, verbose_name='Address line 2')),
                ('gender', models.CharField(choices=[[None, 'Select Gender'], ['Male', 'Male'], ['Female', 'Female'], ['Common', 'Common']], max_length=10, null=True, verbose_name='Gender')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
            ],
            options={
                'verbose_name_plural': 'Vendor Account Details',
            },
        ),
    ]
