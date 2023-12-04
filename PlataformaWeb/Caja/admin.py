from django.contrib import admin
from datetime import timedelta, datetime
from .models import Cuenta, Pago, Cierre, Variable, HistoricoValores
from .forms import PagoForm

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_cliente', 'monto_deberdolar', 'monto_pagado', 'fecha_hora_creacion', 'fecha_hora_pago', 'fecha_hora_ultimo_pago']
    search_fields = ['id', 'id_cliente__nombre', 'id_cliente__apellido']
    date_hierarchy = 'fh_creacion'
    ordering = ('-fh_creacion',)
    readonly_fields = ('fh_creacion', 'fh_pago', 'monto_deberdolar', 'monto_pagado', 'fh_ultimo_pago')

    # Formateo de las fechas
    def fecha_hora_creacion(self, obj):
        hora = obj.fh_creacion - timedelta(hours=4)
        return hora.strftime('%d/%m/%Y %I:%M:%S %p')
    
    def fecha_hora_pago(self, obj):
        if obj.fh_pago:
            hora = obj.fh_pago - timedelta(hours=4)
            return hora.strftime('%d/%m/%Y %I:%M:%S %p')
        return ""

    def fecha_hora_ultimo_pago(self, obj):
        if obj.fh_ultimo_pago:
            hora = obj.fh_ultimo_pago - timedelta(hours=4)
            return hora.strftime('%d/%m/%Y %I:%M:%S %p')
        return ""

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_cuenta', 'met_pago', 'montodolar', 'fecha_hora_pago']
    list_filter = ('met_pago',)
    search_fields = ['id', 'id_cuenta__id']
    date_hierarchy = 'fh_pago'
    ordering = ('-fh_pago',)
    readonly_fields = ('fh_pago',)
    form = PagoForm

    # Formateo de las fechas
    def fecha_hora_pago(self, obj):
        hora = obj.fh_pago - timedelta(hours=4)
        return hora.strftime('%d/%m/%Y %I:%M:%S %p')

@admin.register(Cierre)
class CierreAdmin(admin.ModelAdmin):
    list_display = ['fecha_hora_cierre', 'totalbs_ingreso', 'totaldolar_ingreso', 'totalbs_fianza', 'totaldolar_fianza', 'total_horas', 'total_jugadores', 'totalbs_costoent', 'totaldolar_costoent']
    date_hierarchy = 'fh_cierre'
    ordering = ('-fh_cierre',)
    readonly_fields = ('totalbs_ingreso', 'totaldolar_ingreso', 'totalbs_fianza', 'totaldolar_fianza', 'total_horas', 'total_jugadores', 'totalbs_costoent', 'totaldolar_costoent')

    # Formateo de las fechas
    def fecha_hora_cierre(self, obj):
        hora = obj.fh_cierre
        return hora.strftime('%d/%m/%Y')

@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'valor', 'tipo_dato', 'fecha_hora_actualizacion']
    search_fields = ['id', 'nombre']
    readonly_fields = ('fh_actualizacion',)

    # Formateo de las fechas
    def fecha_hora_actualizacion(self, obj):
        if obj.fh_actualizacion:
            hora = obj.fh_actualizacion - timedelta(hours=4)
            return hora.strftime('%d/%m/%Y %I:%M:%S %p')
        return ""

@admin.register(HistoricoValores)
class HistoricoValoresAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_variable', 'valor']
    search_fields = ['id', 'id_variable__nombre']
    ordering = ('-fh_registro',)

    # Formateo de las fechas
    def fecha_hora_registro(self, obj):
        hora = obj.fh_registro - timedelta(hours=4)
        return hora.strftime('%d/%m/%Y %I:%M:%S %p')