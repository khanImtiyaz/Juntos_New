# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-22 10:17
from __future__ import unicode_literals

import autoslug.fields
import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(error_messages={'unique': 'This email has been already registered.'}, max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(default='', max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, default='', max_length=50, verbose_name='Last name')),
                ('avatar', cloudinary.models.CloudinaryField(blank=True, max_length=5000, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, verbose_name='Mobile')),
                ('mobile_verified', models.BooleanField(default=False, verbose_name='Mobile number Verified')),
                ('mobile_verification_code', models.CharField(blank=True, max_length=12, null=True, verbose_name='Mobile verification code')),
                ('pincode', models.CharField(blank=True, max_length=10, null=True, verbose_name='Vendor pincode')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('login_type', models.CharField(default='normal', max_length=10, verbose_name='Login Type')),
                ('state', models.CharField(blank=True, max_length=50, null=True, verbose_name='State')),
                ('country', models.CharField(blank=True, max_length=50, null=True, verbose_name='Country')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Active')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin')),
                ('is_customer', models.BooleanField(default=False, verbose_name='Customer')),
                ('is_vendor', models.BooleanField(default=False, verbose_name='Vendor')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Admin staff flag')),
                ('is_subadmin', models.BooleanField(default=False, verbose_name='Sub Admin')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('confirmation_code', models.CharField(default='sd', max_length=50, verbose_name='confirmation_code')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=100, populate_from='first_name', unique_with=('created_at',))),
                ('confirmed_on', models.DateTimeField(auto_now=True, verbose_name='confirmed on')),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Banner Tag')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Banner Description')),
                ('status', models.BooleanField(default=False, verbose_name='Mark tick to show on banner')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Image')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banner',
            },
        ),
    ]
