from django.contrib import admin 
from .models import Venta, Cliente, Consola, Juego, Sesion
from Caja.models import Cuenta, Variable
from Inventario.models import Producto
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils.html import format_html
from .forms import SesionForm

## ACCIONES PERSONALIZADAS
def cerrarSesionJuego(modeladmin, request, queryset):
    queryset.update(abierto=False)
    for sesion in queryset:
        consola = Consola.objects.get(numero=sesion.id_consola.numero)
        consola.ocupada = False
        consola.save()
cerrarSesionJuego.short_description = "Cerrar Sesión de Juego"

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_cliente', 'id_producto', 'cantidad', 'fecha_de_compra')
    date_hierarchy = 'fh_venta'
    ordering = ('-fh_venta',)
    readonly_fields = ('id_cuenta',)

    # Ajustar el articulo del mensaje del administardor
    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        # Personalizar el mensaje de éxito según el modelo
        if 'Venta' in message:
            message = format_html("La Compra '{}' se cambió correctamente.", message.split('</a>')[0].split('">')[-1])

        super().message_user(request, message, level, extra_tags, fail_silently)

    # Formateo de las fechas
    def fecha_de_compra(self, obj):
        hora = obj.fh_venta - timedelta(hours=4)
        return hora.strftime('%d/%m/%Y %I:%M:%S %p')

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
        return obj.f_creacion.strftime('%d/%m/%Y')

@admin.register(Consola)
class ConsolaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cant_controles', 'serial', 'fecha_actualizacion', 'ocupada')
    search_fields = ('numero',)
    ordering = ('numero',)
    readonly_fields = ('f_actualizacion','ocupada')

    # Ajustar el articulo del mensaje del administardor
    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        # Personalizar el mensaje de éxito según el modelo
        if 'Consola' in message:
            message = format_html("La Consola '{}' se cambió correctamente.", message.split('</a>')[0].split('">')[-1])

        super().message_user(request, message, level, extra_tags, fail_silently)

    # Formateo de las fechas
    def fecha_actualizacion(self, obj):
        if obj.f_actualizacion:
            return obj.f_actualizacion.strftime('%d/%m/%Y')
        return ""


@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio_compra', 'cantidad', 'genero', 'fecha_compra')
    list_filter = ('genero',)
    search_fields = ('nombre',)
    ordering = ('-f_compra',)

    # Formateo de las fechas
    def fecha_compra(self, obj):
        return obj.f_compra.strftime('%d/%m/%Y')

@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cantidad_horas', 'hora_inicio', 'hora_final', 'id_cliente', 'id_consola', 'abierto')
    time_hierarchy = 'h_inicio'
    ordering = ('-f_sesion','-h_inicio',)
    readonly_fields = ('h_final','id_cuenta','abierto')
    form = SesionForm
    actions = [cerrarSesionJuego]

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
    
    # Campos extras
    def cantidad_horas(self, obj):
        return round((obj.minutos_regalo + obj.cant_minutos)/60, 2)
        

