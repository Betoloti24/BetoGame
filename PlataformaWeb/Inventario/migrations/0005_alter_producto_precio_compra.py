# Generated by Django 4.2.7 on 2023-11-28 18:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Inventario", "0004_alter_producto_cant_invent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="producto",
            name="precio_compra",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=4,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
    ]
