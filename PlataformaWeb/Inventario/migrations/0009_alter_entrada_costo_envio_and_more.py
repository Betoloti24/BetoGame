# Generated by Django 4.2.7 on 2024-07-27 19:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0008_entrada_costo_envio_entrada_costo_mercancia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='costo_envio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_compra',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_venta',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
