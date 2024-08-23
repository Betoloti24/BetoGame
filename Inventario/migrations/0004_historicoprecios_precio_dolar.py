# Generated by Django 4.2.7 on 2024-08-23 14:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0003_entrada_costo_envio_dolar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicoprecios',
            name='precio_dolar',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5, validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
    ]