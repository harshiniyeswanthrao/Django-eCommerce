# Generated by Django 5.0.3 on 2024-08-26 07:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0008_remove_product_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sizes', models.CharField(max_length=255)),
                ('colors', models.CharField(max_length=255)),
                ('offers', models.CharField(max_length=255)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='first_app.product')),
            ],
        ),
    ]
