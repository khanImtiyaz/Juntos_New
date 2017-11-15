# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-15 07:25
from __future__ import unicode_literals

import cloudinary.models
import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0041_auto_20171114_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', colorfield.fields.ColorField(default='#FF0000', max_length=18)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productColor', to='Juntos.ProductsManagement')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_images', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Image')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('product_colr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_color_images', to='Juntos.ProductColor')),
            ],
            options={
                'verbose_name_plural': 'Manage Product Image',
            },
        ),
    ]