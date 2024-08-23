from django import forms
from .models import Pago, Cuenta, Cierre, Variable

# Creamos un formulario con el modelo de Cuentas
class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = '__all__'
        labels = {
            'id_cliente': 'Cliente',
            'monto_deber': 'Deuda (Bs)',
            'monto_pagado': 'Pagado (Bs)',
            'monto_deber_dolar': 'Deuda ($)',
            'monto_pagado_dolar': 'Pagado ($)',
            'fh_creacion': 'Fecha de Creación',
            'fh_ultimo_pago': 'Fecha de Último Pago',
            'fh_pago': 'Fecha de Cierre', 
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'
        labels = {
            'id_cuenta': 'Cuenta',
            'monto': 'Monto a Pagar (Bs)',
            'monto_dolar': 'Monto a Pagar ($)',
            'met_pago': 'Método de Pago',
            'fh_pago': 'Fecha de Pago',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las opciones del campo de cuenta para mostrar solo cuentas no pagadas
        cuentas_no_pagadas = Cuenta.objects.filter(fh_pago=None).order_by("id_cliente__nombre")
        if self.fields:
            self.fields['id_cuenta'].queryset = cuentas_no_pagadas

class CierreForm(forms.ModelForm):
    class Meta:
        model = Cierre
        fields = '__all__'
        labels = {
            'id': 'Cierre',
            'fh_cierre': 'Fecha de Cierre',
            'totalbs_ingreso': 'Ingreso (Bs)',
            'totaldolar_ingreso': 'Ingreso ($)',
            'totalbs_fianza': 'Fianza (Bs)',
            'totaldolar_fianza': 'Fianza ($)',
            'totalbs_costoent': 'Costo de Mercancia (Bs)',
            'totaldolar_costoent': 'Costo de Mercancia ($)',
            'total_jugadores': 'Total de Jugadores',
            'total_horas': 'Total de Horas',
            'total_minutos': 'Total de Minutos',
        }

class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = '__all__'
        labels = {
            'id': 'Variable',
            'nombre': 'Nombre',
            'valor': 'Valor',
            'tipo_dato': 'Tipo de Dato',
            'fh_actualizacion': 'Fecha de Actualización',
        }