# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-11 13:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Juntos', '0031_billingaddress_shippingaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_payment_type', models.CharField(max_length=20, verbose_name='Order payment method')),
                ('order_number', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Order Number')),
                ('order_date', models.DateTimeField(auto_now=True, verbose_name='Order Date')),
                ('delivery_date', models.DateField(verbose_name='Delivery Date')),
                ('pickup_date', models.DateField(auto_now=True, verbose_name='Pickup Date')),
                ('delivery_status', models.BooleanField(default=False, verbose_name='Order Delivery Status')),
                ('expected_delivery_time', models.IntegerField(blank=True, default=8, null=True, verbose_name='Expected Delivery Time In Day')),
                ('base_price', models.FloatField(verbose_name='Total Base Price')),
                ('shipping_charge', models.FloatField(verbose_name='Shipping Charges')),
                ('shipping_percent', models.FloatField(blank=True, default=5.0, null=True, verbose_name='Shipping Percent')),
                ('tax_charges', models.FloatField(verbose_name='Tax Charges')),
                ('tax_percent', models.FloatField(blank=True, default=18.0, null=True, verbose_name='tax Percent')),
                ('discount', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Discount')),
                ('total', models.FloatField(verbose_name='Total Order Price')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_title', models.CharField(blank=True, max_length=50, verbose_name='offer Title')),
                ('offer_details', models.CharField(blank=True, max_length=200, verbose_name='offer Details')),
                ('offer_start_date_time', models.DateTimeField()),
                ('offer_end_date_time', models.DateTimeField()),
                ('original_price', models.IntegerField()),
                ('offer_price', models.IntegerField(help_text='Offer price should not more then original price of product.')),
                ('offer_image', models.ImageField(blank=True, help_text='Please keep Offer image different to product image.', max_length=5000, null=True, upload_to='')),
                ('offer_quantity', models.IntegerField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_product', to='Juntos.ProductsManagement')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_sub_category', to='Juntos.SubCategory')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_vendor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_color', models.IntegerField(blank=True, null=True)),
                ('product_size', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(default=1, verbose_name='Product quantity')),
                ('base_price', models.FloatField(blank=True, null=True, verbose_name='Base Price')),
                ('shipping_charge', models.FloatField(verbose_name='Shipping Charges')),
                ('shipping_percent', models.FloatField(blank=True, default=5.0, null=True, verbose_name='Shipping Percent')),
                ('tax_charges', models.FloatField(verbose_name='Tax Charges')),
                ('tax_percent', models.FloatField(blank=True, default=18.0, null=True, verbose_name='tax Percent')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='Total Price')),
                ('delivery_date', models.DateField(blank=True, null=True, verbose_name='Delivery Date')),
                ('delivery_status', models.CharField(blank=True, default='Pending', max_length=20, verbose_name='Order Item Delivery Status')),
                ('order_cancel_request', models.BooleanField(default=False, verbose_name='Order Cancel Request')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='Juntos.CustomerOrder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='Juntos.ProductsManagement')),
                ('product_offer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_offer', to='Juntos.Offer')),
            ],
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='billing_country_abbreviation',
            field=models.CharField(max_length=20, verbose_name='Billing Country Abbreviation'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_country_abbreviation',
            field=models.CharField(max_length=20, verbose_name='Shipping Country Abbreviation'),
        ),
        migrations.AddField(
            model_name='customerorder',
            name='shipping_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_address', to='Juntos.ShippingAddress'),
        ),
    ]
