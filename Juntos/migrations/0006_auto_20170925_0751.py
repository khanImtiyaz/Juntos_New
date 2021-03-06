# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-25 07:51
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0005_auto_20170925_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_category',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='sub_category_name', unique_with=('sub_category_tag',)),
        ),
        migrations.AlterField(
            model_name='sub_category',
            name='sub_category_flage',
            field=models.CharField(blank=True, choices=[[None, 'Select Flage'], ['CLOTH', 'Clothes'], ['SHOES', 'Shoes or Boots']], help_text='Is Cloth or Shoes ?', max_length=10, null=True, verbose_name='Sub Category Flag'),
        ),
    ]
