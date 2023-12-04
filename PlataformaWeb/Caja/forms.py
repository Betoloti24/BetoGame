from django import forms
from .models import Pago, Cuenta

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las opciones del campo de cuenta para mostrar solo cuentas no pagadas
        cuentas_no_pagadas = Cuenta.objects.filter(fh_pago=None)
        if self.fields:
            self.fields['id_cuenta'].queryset = cuentas_no_pagadas