# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-03 09:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0022_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whislist_product', to='Juntos.ProductsManagement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whislist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
