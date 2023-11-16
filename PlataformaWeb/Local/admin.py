from django.contrib import admin
from .models import Compra, Cliente, Consola, Juego, Sesion
from Inventario.models import Producto
from datetime import datetime
from django.contrib import messages
from django.utils.html import format_html

# Register your models here.

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_producto', 'id_cliente', 'cantidad', 'monto', 'met_pago', 'fecha_creacion')
    list_filter = ('met_pago',)
    date_hierarchy = 'fh_compra'
    ordering = ('-fh_compra',)

    # # Actualizar cantidad en inventario del producto
    # def save_model(self, request, obj, form, change):
    #     # Guardar el modelo
    #     super().save_model(request, obj, form, change)

    #     # Disminuir la cantidad en inventario del producto
    #     producto = obj.id_producto
    #     cantidad_compra = obj.cantidad

    #     if producto.cant_invent >= cantidad_compra:
    #         producto.cant_invent -= cantidad_compra
    #         producto.save()
    #     else:
    #         # Revertir la transacción si la cantidad en inventario es insuficiente
    #         obj.delete()
    #         message = f"No se puede vender {cantidad_compra} productos. Cantidad insuficiente en inventario ({producto.cant_invent})."
    #         self.message_user(request, message, level='ERROR')

    # Ajustar el articulo del mensaje del administardor
    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        # Personalizar el mensaje de éxito según el modelo
        if 'Sesion' in message:
            message = format_html("La Sesion '{}' se cambió correctamente.", message.split('</a>')[0].split('">')[-1])

        super().message_user(request, message, level, extra_tags, fail_silently)

    # Formateo de las fechas
    def fecha_creacion(self, obj):
        return obj.fh_compra.strftime('%Y-%m-%d')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('ci', 'nombre', 'apellido', 'telefono', 'fecha_creacion')
    list_filter = ('genero',)
    search_fields = ('nombre', 'apellido', 'correo')
    date_hierarchy = 'f_creacion'
    ordering = ('-f_creacion',)
    readonly_fields = ('f_actualizacion',)

    # Formateo de las fechas
    def fecha_creacion(self, obj):
        return obj.f_creacion.strftime('%Y-%m-%d')

@admin.register(Consola)
class ConsolaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cant_controles', 'serial', 'fecha_actualizacion')
    search_fields = ('numero',)
    ordering = ('numero',)
    readonly_fields = ('f_actualizacion',)

    # Ajustar el articulo del mensaje del administardor
    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        # Personalizar el mensaje de éxito según el modelo
        if 'Sesion' in message:
            message = format_html("La Sesion '{}' se cambió correctamente.", message.split('</a>')[0].split('">')[-1])

        super().message_user(request, message, level, extra_tags, fail_silently)

    # Formateo de las fechas
    def fecha_actualizacion(self, obj):
        if obj.f_actualizacion:
            return obj.f_actualizacion.strftime('%Y-%m-%d')
        return ""


@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio_compra', 'cantidad', 'genero', 'fecha_compra')
    list_filter = ('genero',)
    search_fields = ('nombre',)
    ordering = ('-f_compra',)

    # Formateo de las fechas
    def fecha_compra(self, obj):
        return obj.f_compra.strftime('%Y-%m-%d')

@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ('id', 'hora_inicio', 'hora_final', 'id_cliente', 'id_consola')
    list_filter = ('met_pago',)
    time_hierarchy = 'h_inicio'
    ordering = ('-f_sesion','-h_inicio',)
    readonly_fields = ('h_final',)

    # Ajustar el articulo del mensaje del administardor
    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        # Personalizar el mensaje de éxito según el modelo
        if 'Sesion' in message:
            message = format_html("La Sesion '{}' se cambió correctamente.", message.split('</a>')[0].split('">')[-1])

        super().message_user(request, message, level, extra_tags, fail_silently)

    # Formateo de las fechas y horas
    def hora_inicio(self, obj):
        return obj.h_inicio.strftime("%I:%M:%S %p")
    
    def hora_final(self, obj):
        return obj.h_final.strftime("%I:%M:%S %p")
        


