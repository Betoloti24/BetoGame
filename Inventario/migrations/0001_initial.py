# Generated by Django 4.2.7 on 2024-07-27 22:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=20)),
                ('precio_venta', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MinValueValidator(0)])),
                ('precio_compra', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('cant_invent', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('tipo_producto', models.CharField(choices=[('bebida', 'Bebida'), ('dulce', 'Dulce'), ('salado', 'Salado'), ('otro', 'Otro')], max_length=6)),
                ('f_creacion', models.DateField(auto_now_add=True)),
                ('f_actualizacion', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['-f_creacion'],
            },
        ),
        migrations.CreateModel(
            name='HistoricoPrecios',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(1)])),
                ('fh_registro', models.DateTimeField(auto_now_add=True)),
                ('vigente', models.BooleanField(default=True)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventario.producto')),
            ],
            options={
                'verbose_name': 'Historico de Precios',
                'verbose_name_plural': 'Historicos de Precios',
                'ordering': ['-fh_registro'],
            },
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('costo_punidad', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(1)])),
                ('costo_mercancia', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(1)])),
                ('costo_envio', models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)])),
                ('fh_registro', models.DateTimeField(auto_now_add=True)),
                ('tipo_entrada', models.CharField(choices=[('compra', 'Comprado'), ('produccion', 'Producido')], max_length=10)),
                ('cant_ingresada', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('proveedor', models.CharField(blank=True, max_length=20, null=True)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventario.producto')),
            ],
            options={
                'verbose_name': 'Entrada',
                'verbose_name_plural': 'Entradas',
                'ordering': ['-fh_registro'],
            },
        ),
    ]
