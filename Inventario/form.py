from django import forms
from .models import Entrada, Producto, HistoricoPrecios

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        labels = {
            'nombre': 'Nombre',
            'tipo_producto': 'Tipo de Producto',
            'precio_venta': 'Precio de Venta (Bs)',
            'f_creacion': 'Fecha de Creación (Bs)',
            'f_actualizacion': 'Fecha de Actualización',
            'precio_compra': 'Precio de Compra (Bs)',
            'cant_invent': 'Cantidad en Inventario'
        }

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = '__all__'
        labels = {
            'id_producto': 'Producto',
            'costo_punidad': 'Costo por Unidad (Bs)',
            'cant_ingresada': 'Cantidad Ingresada',
            'costo_mercancia': 'Costo de Mercancía (Bs)',
            'costo_envio': 'Costo de Envío (Bs)',
            'tipo_entrada': 'Tipo de Entrada',
            'fh_registro': 'Fecha de Registro',
            'proveedor': 'Proveedor'
        }

class HistoricoPreciosForm(forms.ModelForm):
    class Meta:
        model = HistoricoPrecios
        fields = '__all__'
        labels = {
            'id_producto': 'Producto',
            'precio': 'Precio (Bs)',
            'fh_registro': 'Fecha de Registro',
            'vigente': '¿Vigente?'
        }