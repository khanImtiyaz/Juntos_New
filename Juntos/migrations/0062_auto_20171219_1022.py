# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-19 10:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0061_auto_20171219_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertismentReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=100, verbose_name='Customer Reviews')),
                ('rating', models.FloatField(blank=True, default=0, verbose_name='Rating value')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('advertisement_reviews', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_adv', to='Juntos.Advertisement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_gvn', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Advertisement Reviews',
            },
        ),
        migrations.AlterField(
            model_name='customerreview',
            name='content',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Customer Reviews'),
        ),
    ]
