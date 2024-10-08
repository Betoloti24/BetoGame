from django import forms
from .models import Sesion, Consola, Juego, Venta, Cliente

class SesionForm(forms.ModelForm):
    class Meta:
        model = Sesion
        fields = '__all__'
        labels = {
            'h_inicio': 'Hora de Inicio',
            'h_final': 'Hora de Fin',
            'f_sesion': 'Fecha de Sesión',
            'id_cliente': 'Cliente',
            'id_consola': 'Consola',
            'id_cuenta': 'Cuenta',
            'minutos_regalo': 'Minutos de Regalo',
            'abierto': 'Abierto',
            'cant_minutos': 'Cantidad de Minutos',
            'cant_personas': 'Cantidad de Personas',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_cliente'].queryset = self.fields['id_cliente'].queryset.order_by('nombre')  # Reemplaza 'nombre' por el campo que define el nombre del cliente

class ConsolaForm(forms.ModelForm):
    class Meta:
        model = Consola
        fields = '__all__'
        labels = {
            "numero": "Número",
            "cant_controles": "Cantidad de Controles",
            "ocupada": "Ocupada",
            "juegos_instalados": "Juegos Instalados",
            "serial": "Serial",
            "f_actualizacion": "Fecha de Actualización",
        }

class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = '__all__'
        labels = {
            'id': 'ID',
            'nombre': 'Nombre',
            'f_compra': 'Fecha de Compra',
            'precio_compra_dolar': 'Precio de Compra',
            'cantidad': 'Cantidad',
            'genero': 'Género',
            'tipo': 'Tipo',
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'
        labels = {
            'id_cliente': 'Cliente',
            'id_producto': 'Producto',  
            'cantidad': 'Cantidad',
            'fh_venta': 'Fecha de Venta',
            'id_cuenta': 'Cuenta'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.fields) != 0:
            self.fields['id_cliente'].queryset = self.fields['id_cliente'].queryset.order_by('nombre')
            self.fields['id_producto'].queryset = self.fields['id_producto'].queryset.order_by('nombre')

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        labels = {
            "ci": "C.I",
            "nombre": "Nombre",
            "apellido": "Apellido",
            "genero": "Género",
            "f_nacimiento": "Fecha de Nacimiento",
            "ubicacion": "Ubicación",
            "telefono": "Teléfono",
            "correo": "Correo",
            "minutos_favor": "Minutos a Favor",
            "f_creacion": "Fecha de Creación",
            "f_actualizacion": "Fecha de Actualización",
        }
    