# Generated by Django 4.2.7 on 2024-07-27 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cierre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fh_cierre', models.DateField(unique=True)),
                ('totalbs_ingreso', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('totaldolar_ingreso', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('totalbs_fianza', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('totaldolar_fianza', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('totalbs_costoent', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('totaldolar_costoent', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('total_jugadores', models.DecimalField(decimal_places=0, default=0.0, max_digits=2)),
                ('total_horas', models.DecimalField(decimal_places=0, default=0.0, max_digits=3)),
            ],
            options={
                'verbose_name': 'Cierre',
                'verbose_name_plural': 'Cierres',
            },
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('monto_deberdolar', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('monto_pagado', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('fh_creacion', models.DateTimeField(auto_now_add=True)),
                ('fh_ultimo_pago', models.DateTimeField(blank=True, null=True)),
                ('fh_pago', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name': 'Cuenta',
                'verbose_name_plural': 'Cuentas',
            },
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('valor', models.CharField(max_length=15)),
                ('tipo_dato', models.CharField(choices=[('Entero', 'Entero'), ('Decimal', 'Decimal'), ('Texto', 'Texto')], max_length=10)),
                ('fh_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Variable',
                'verbose_name_plural': 'Variables',
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('met_pago', models.CharField(choices=[('efectivodolar', 'Efectivo $'), ('efectivobs', 'Efectivo Bs'), ('tarjeta', 'Tarjeta'), ('pago_movil', 'Pago Móvil')], max_length=13)),
                ('montodolar', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fh_pago', models.DateTimeField(auto_now_add=True)),
                ('id_cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Caja.cuenta')),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
            },
        ),
        migrations.CreateModel(
            name='HistoricoValores',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('valor', models.CharField(max_length=15)),
                ('fh_registro', models.DateTimeField(auto_now_add=True)),
                ('vigente', models.BooleanField(default=True)),
                ('id_variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Caja.variable')),
            ],
            options={
                'verbose_name': 'Histórico de Valores',
                'verbose_name_plural': 'Históricos de Valores',
            },
        ),
    ]