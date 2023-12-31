# Generated by Django 4.2.7 on 2023-11-23 14:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Inventario", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="producto",
            name="precio_compra",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=4,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
            preserve_default=False,
        ),
    ]
