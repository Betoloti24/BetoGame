from django.contrib import admin
from datetime import timedelta
from Caja.models import Cuenta, Pago, Cierre, Variable, HistoricoValores
from Caja.forms import PagoForm, CuentaForm, CierreForm, VariableForm

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'set_id_cliente', 'set_monto_deber', 'set_monto_pagado', 'set_monto_deber_dolar', 'set_monto_pagado_dolar', 'set_fecha_hora_creacion', 'set_fecha_hora_ultimo_pago', 'set_fecha_hora_pago']
    search_fields = ['id', 'id_cliente__nombre', 'id_cliente__apellido', 'id_cliente__ci']
    date_hierarchy = 'fh_creacion'
    list_filter = ('fh_pago',)
    ordering = ('-fh_pago', '-fh_ultimo_pago', '-fh_creacion')
    readonly_fields = ('fh_creacion', 'fh_pago', 'monto_deber', 'monto_pagado', 'fh_ultimo_pago', "id_cliente")

    # Formateo de los campos
    def set_fecha_hora_creacion(self, obj):
        hora = obj.fh_creacion - timedelta(hours=4)
        return hora.strftime('%d/%m/%Y %I:%M:%S %p')
    def set_fecha_hora_pago(self, obj):
        if obj.fh_pago:
            hora = obj.fh_pago - timedelta(hours=4)
            return hora.strftime('%d/%m/%Y %I:%M:%S %p')
        return ""
    def set_fecha_hora_ultimo_pago(self, obj):
        if obj.fh_ultimo_pago:
            hora = obj.fh_ultimo_pago - timedelta(hours=4)
            return hora.strftime('%d/%m/%Y %I:%M:%S %p')
        return ""
    def set_monto_pagado(self, obj):
        return f"{obj.monto_pagado:.2f}Bs"
    def set_monto_deber(self, obj):
        return f"{obj.monto_deber:.2f}Bs"
    def set_monto_deber_dolar(self, obj):
        return f"{obj.monto_deber_dolar:.2f}$"
    def set_monto_pagado_dolar(self, obj):
        return f"{obj.monto_pagado_dolar:.2f}$"
    def set_id_cliente(self, obj):
        return f"{obj.id_cliente.nombre} {obj.id_cliente.apellido}"
    
    # Asignacion de los nombres a los campos
    set_fecha_hora_creacion.short_description = 'Fecha de Creación'
    set_fecha_hora_pago.short_description = 'Fecha Cierre de la Cuenta'
    set_fecha_hora_ultimo_pago.short_description = 'Fecha del Último Pago'
    set_monto_pagado.short_description = 'Pagado (Bs)'
    set_monto_deber.short_description = 'Deuda (Bs)'
    set_monto_deber_dolar.short_description = 'Deuda ($)'
    set_monto_pagado_dolar.short_description = 'Pagado ($)'
    set_id_cliente.short_description = 'Cliente'

    form = CuentaForm

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'set_id_cuenta', 'set_monto', 'set_monto_dolar', 'set_met_pago', 'set_fecha_hora_pago']
    list_filter = ('met_pago',)
    search_fields = ['id', 'id_cuenta__id']
    date_hierarchy = 'fh_pago'
    ordering = ('-fh_pago',)
    readonly_fields = ('fh_pago', 'monto_dolar')

    # Formateo de los campos
    def set_fecha_hora_pago(self, obj):
        hora = obj.fh_pago - timedelta(hours=4)
        return hora.strftime('%d/%m/%Y %I:%M:%S %p')
    def set_monto(self, obj):
        return f"{obj.monto:.2f}Bs" if obj.monto else "0.0Bs"
    def set_monto_dolar(self, obj):
        return f"{obj.monto_dolar:.2f}$" if obj.monto_dolar else "0.0$"
    def set_id_cuenta(self, obj):
        return f"Cuenta {obj.id_cuenta.id}: {obj.id_cuenta.id_cliente.nombre} {obj.id_cuenta.id_cliente.apellido}"
    def set_met_pago(self, obj):
        met_pago_dict = {
            'efectivodolar': 'Efectivo ($)',
            'efectivobs': 'Efectivo (Bs)',
            'tarjeta': 'Tarjeta',
            'pago_movil': 'Pago Móvil'
        }
        return met_pago_dict.get(obj.met_pago, obj.met_pago)
    
    # Asignacion de los nombres a los campos
    set_fecha_hora_pago.short_description = 'Fecha de Pago'
    set_monto.short_description = 'Pagado (Bs)'
    set_monto_dolar.short_description = 'Pagado ($)'
    set_id_cuenta.short_description = 'Cuenta'
    set_met_pago.short_description = 'Método de Pago'

    form = PagoForm

@admin.register(Cierre)
class CierreAdmin(admin.ModelAdmin):
    list_display = ['set_fecha_hora_cierre', 'set_totalbs_ingreso', 'set_totaldolar_ingreso', 'set_totalbs_fianza', 'set_totaldolar_fianza', 'set_total_horas', 'set_total_minutos', 'set_total_jugadores', 'set_totalbs_costoent', 'set_totaldolar_costoent']
    date_hierarchy = 'fh_cierre'
    ordering = ('-fh_cierre',)
    readonly_fields = ('totalbs_ingreso', 'totaldolar_ingreso', 'totalbs_fianza', 'totaldolar_fianza', 'total_horas', 'total_minutos', 'total_jugadores', 'totalbs_costoent', 'totaldolar_costoent')

    # Formateo de los campos
    def set_fecha_hora_cierre(self, obj):
        hora = obj.fh_cierre
        return hora.strftime('%d/%m/%Y')
    def set_totalbs_ingreso(self, obj):
        return f"{obj.totalbs_ingreso:.2f}Bs"
    def set_totaldolar_ingreso(self, obj):
        return f"{obj.totaldolar_ingreso:.2f}$"
    def set_totalbs_fianza(self, obj):
        return f"{obj.totalbs_fianza:.2f}Bs"
    def set_totaldolar_fianza(self, obj):
        return f"{obj.totaldolar_fianza:.2f}$"
    def set_totalbs_costoent(self, obj):
        return f"{obj.totalbs_costoent:.2f}Bs"
    def set_totaldolar_costoent(self, obj):
        return f"{obj.totaldolar_costoent:.2f}$"
    def set_total_horas(self, obj):
        return f"{obj.total_horas} horas"
    def set_total_minutos(self, obj):
        return f"{obj.total_minutos} min"
    def set_total_jugadores(self, obj):
        return f"{obj.total_jugadores} jugadores"
    
    # Asignacion de los nombres a los campos
    set_fecha_hora_cierre.short_description = 'Fecha de Cierre'
    set_totalbs_ingreso.short_description = 'Total Ingreso (Bs)'
    set_totaldolar_ingreso.short_description = 'Total Ingreso ($)'
    set_totalbs_fianza.short_description = 'Total Fiado (Bs)'
    set_totaldolar_fianza.short_description = 'Total Fiado ($)'
    set_totalbs_costoent.short_description = 'Total Costo Mercancía (Bs)'
    set_totaldolar_costoent.short_description = 'Total Costo de Mercacía ($)'
    set_total_horas.short_description = 'Total de Horas'    
    set_total_minutos.short_description = 'Total de Minutos'    

    form = CierreForm

@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = ['id', 'set_nombre', 'set_tipo_dato', 'set_valor', 'set_fecha_hora_actualizacion']
    search_fields = ['id', 'nombre']
    readonly_fields = ('fh_actualizacion',)

    # Formateo de los campos
    def set_fecha_hora_actualizacion(self, obj):
        if obj.fh_actualizacion:
            hora = obj.fh_actualizacion - timedelta(hours=4)
            return hora.strftime('%d/%m/%Y %I:%M:%S %p')
        return ""
    def set_valor(self, obj):
        return obj.valor
    def set_tipo_dato(self, obj):
        return obj.tipo_dato
    def set_nombre(self, obj):
        return obj.nombre
    
    # Asignacion de los nombres a los campos
    set_fecha_hora_actualizacion.short_description = 'Fecha de Actualización'
    set_valor.short_description = 'Valor'
    set_tipo_dato.short_description = 'Tipo de Dato'
    set_nombre.short_description = 'Nombre'

    form = VariableForm

@admin.register(HistoricoValores)
class HistoricoValoresAdmin(admin.ModelAdmin):
    list_display = ['id', 'set_id_variable', 'set_valor', 'set_fecha_hora_registro', 'set_vigente']
    search_fields = ['id', 'id_variable__nombre']
    ordering = ('-fh_registro',)

    # Formateo de los campos
    def set_fecha_hora_registro(self, obj):
        hora = obj.fh_registro - timedelta(hours=4)
        return hora.strftime('%d/%m/%Y %I:%M:%S %p')
    def set_valor(self, obj):
        return obj.valor
    def set_id_variable(self, obj):
        return obj.id_variable.nombre
    def set_vigente(self, obj):
        return f"Si" if obj.vigente else "No"
    
    # Asignacion de los nombres a los campos
    set_fecha_hora_registro.short_description = 'Fecha de Registro'
    set_valor.short_description = 'Valor'
    set_id_variable.short_description = 'Variable'
    set_vigente.short_description = '¿Vigente?'