# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-22 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0069_auto_20180122_0530'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.CharField(choices=[['CLOTH', 'Clothes'], ['SHOES', 'Shoes or Boots']], max_length=40, verbose_name='Product Family')),
                ('size', models.CharField(max_length=5, verbose_name='Size')),
            ],
        ),
    ]
