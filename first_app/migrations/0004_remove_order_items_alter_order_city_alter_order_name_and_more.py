# Generated by Django 5.0.3 on 2024-08-17 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0003_remove_product_category_product_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
