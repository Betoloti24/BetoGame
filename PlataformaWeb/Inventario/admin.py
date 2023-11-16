from django.contrib import admin
from .models import Producto
from django.contrib import messages
from django.utils.html import format_html

## Registro de los modelos por decorador

# Producto
from django.contrib import admin
from .models import Producto, HistoricoPrecios, Entrada

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio_venta', 'cant_invent', 'tipo_producto', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('tipo_producto',)
    search_fields = ('nombre',)
    date_hierarchy = 'f_creacion'
    ordering = ('-f_creacion',)
    readonly_fields = ('f_actualizacion',)

    # Formateo de las fechas
    def fecha_creacion(self, obj):
        return obj.f_creacion.strftime('%Y-%m-%d')
    
    def fecha_actualizacion(self, obj):
        if obj.f_actualizacion:
            return obj.f_actualizacion.strftime('%Y-%m-%d')
        return ""

@admin.register(HistoricoPrecios)
class HistoricoPreciosAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_producto', 'precio', 'fecha_creacion', 'vigente')
    list_filter = ('vigente',)
    date_hierarchy = 'fh_registro'
    ordering = ('-fh_registro',)
    readonly_fields = ('vigente',)

    # Formateo de las fechas
    def fecha_creacion(self, obj):
        return obj.fh_registro.strftime('%Y-%m-%d')

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_producto', 'costo', 'tipo_entrada', 'cant_ingresada', 'fecha_creacion')
    list_filter = ('tipo_entrada',)
    date_hierarchy = 'fh_registro'
    ordering = ('-fh_registro',)

    # Ajustar el articulo del mensaje del administardor
    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        # Personalizar el mensaje de éxito según el modelo
        if 'Sesion' in message:
            message = format_html("La Sesion '{}' se cambió correctamente.", message.split('</a>')[0].split('">')[-1])

        super().message_user(request, message, level, extra_tags, fail_silently)

    # Formateo de las fechas
    def fecha_creacion(self, obj):
        return obj.fh_registro.strftime('%Y-%m-%d')


