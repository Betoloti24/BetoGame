# Generated by Django 4.2.7 on 2024-07-27 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Caja', '0011_auto_20240727_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='met_pago',
            field=models.CharField(choices=[('efectivodolar', 'Efectivo $'), ('efectivobs', 'Efectivo Bs'), ('tarjeta', 'Tarjeta'), ('pago_movil', 'Pago Móvil')], max_length=13),
        ),
    ]
