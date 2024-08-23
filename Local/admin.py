from datetime import timedelta
from django.contrib import admin 
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils.html import format_html

from Local.forms import SesionForm, ConsolaForm, JuegoForm, ClienteForm, VentaForm
from Local.models import Venta, Cliente, Consola, Juego, Sesion

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
    list_display = ('id', 'set_id_cliente', 'set_id_producto', 'set_cantidad', 'set_fecha_de_venta')
    date_hierarchy = 'fh_venta'
    ordering = ('-fh_venta',)
    readonly_fields = ('id_cuenta', )

    # Ajustar el articulo del mensaje del administardor
    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        # Personalizar el mensaje de éxito según el modelo
        if 'Venta' in message:
            message = format_html("La Venta '{}' se cambió correctamente.", message.split('</a>')[0].split('">')[-1])

        super().message_user(request, message, level, extra_tags, fail_silently)

    # Formateo de los campos
    def set_fecha_de_venta(self, obj):
        hora = obj.fh_venta - timedelta(hours=4)
        return hora.strftime('%d/%m/%Y %I:%M:%S %p')
    def set_id_cliente(self, obj):
        return f"{obj.id_cliente.nombre} {obj.id_cliente.apellido}"
    def set_id_producto(self, obj):
        return obj.id_producto.nombre
    def set_cantidad(self, obj):
        return f"{obj.cantidad} unidades"
    
    # Asignacion de los nombres a los campos
    set_fecha_de_venta.short_description = 'Fecha de la Venta'
    set_id_cliente.short_description = 'Cliente'
    set_id_producto.short_description = 'Producto'
    set_cantidad.short_description = 'Cantidad'       

    form = VentaForm

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('set_ci', 'set_nombre', 'set_telefono', 'set_fecha_creacion')
    list_filter = ('genero',)
    search_fields = ('nombre', 'apellido', 'correo', 'telefono', 'ci')
    date_hierarchy = 'f_creacion'
    ordering = ('-f_creacion',)
    readonly_fields = ('f_actualizacion',)

    # Formateo de los campos
    def set_ci(self, obj):
        return obj.ci
    def set_nombre(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    def set_telefono(self, obj):
        return obj.telefono
    def set_fecha_creacion(self, obj):
        return obj.f_creacion.strftime('%d/%m/%Y')
    
    # Asignacion de etiquetas
    set_fecha_creacion.short_description = 'Fecha de Creación'
    set_nombre.short_description = 'Nombre Completo'
    set_telefono.short_description = 'Teléfono'
    set_ci.short_description = 'C.I.'

    form = ClienteForm

@admin.register(Consola)
class ConsolaAdmin(admin.ModelAdmin):
    list_display = ('set_numero', 'set_cant_controles', 'set_serial', 'set_fecha_actualizacion', 'set_ocupada')
    search_fields = ('numero',)
    ordering = ('numero',)
    readonly_fields = ('f_actualizacion','ocupada')

    # Ajustar el articulo del mensaje del administardor
    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        # Personalizar el mensaje de éxito según el modelo
        if 'Consola' in message:
            message = format_html("La Consola '{}' se cambió correctamente.", message.split('</a>')[0].split('">')[-1])

        super().message_user(request, message, level, extra_tags, fail_silently)

    # Formateo de los campos
    def set_fecha_actualizacion(self, obj):
        if obj.f_actualizacion:
            return obj.f_actualizacion.strftime('%d/%m/%Y')
        return ""
    def set_numero(self, obj):
        return obj.numero
    def set_cant_controles(self, obj):
        return obj.cant_controles
    def set_serial(self, obj):
        return obj.serial
    def set_ocupada(self, obj):
        return "Ocupado" if obj.ocupada else "Libre"
    
    # Actualizamos las etiquetas
    set_fecha_actualizacion.short_description = 'Fecha de Actualización'
    set_numero.short_description = 'Número'
    set_cant_controles.short_description = 'Cantidad de Controles'
    set_serial.short_description = 'Serial'
    set_ocupada.short_description = 'Estado'

    form = ConsolaForm

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('set_id', 'set_nombre', 'set_precio_compra_dolar', 'set_cantidad', 'set_genero', 'set_fecha_compra')
    list_filter = ('genero',)
    search_fields = ('nombre',)
    ordering = ('-f_compra',)

    # Formateo de los campos
    def set_fecha_compra(self, obj):
        return obj.f_compra.strftime('%d/%m/%Y')
    def set_nombre(self, obj):
        return obj.nombre
    def set_id(self, obj):
        return obj.id
    def set_precio_compra_dolar(self, obj):
        return f"{obj.precio_compra_dolar}$"
    def set_cantidad(self, obj):
        return obj.cantidad
    def set_genero(self, obj):
        generos = {
            'accion': 'Acción',
            'aventura': 'Aventura',
            'deportes': 'Deportes',
            'estrategia': 'Estrategia',
            'otros': 'Otros',
        }
        return generos.get(obj.genero, obj.genero)
    
    # Actualizar etiquetas
    set_fecha_compra.short_description = "Fecha de Compra"
    set_nombre.short_description = "Nombre"
    set_id.short_description = "ID"
    set_precio_compra_dolar.short_description = "Precio de Compra ($)"
    set_cantidad.short_description = "Cantidad"
    set_genero.short_description = "Género"

    form = JuegoForm

@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ('set_id', 'set_cantidad_horas', 'set_cantidad_minutos', 'set_hora_inicio', 'set_hora_final', 'set_id_cliente', 'set_id_consola', 'set_abierto')
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

    # Formateo de campos
    def set_hora_inicio(self, obj):
        return obj.h_inicio.strftime("%I:%M:%S %p")
    def set_hora_final(self, obj):
        return obj.h_final.strftime("%I:%M:%S %p")
    def set_cantidad_horas(self, obj):
        return f"{round((obj.minutos_regalo + obj.cant_minutos)/60, 2)} horas"
    def set_cantidad_minutos(self, obj):
        return f"{obj.minutos_regalo + obj.cant_minutos} minutos"
    def set_id(self, obj):
        return obj.id
    def set_id_cliente(self, obj):
        return f"{obj.id_cliente.nombre} {obj.id_cliente.apellido}"
    def set_id_consola(self, obj):
        return f"Consola N°{obj.id_consola}"
    def set_abierto(self, obj):
        return "Abierta" if obj.abierto else "Cerrada"
    
    # Actualizar etiquetas
    set_hora_inicio.short_description = "Hora de Inicio"
    set_hora_final.short_description = "Hora de Finalización"
    set_cantidad_horas.short_description = "Cantidad de Horas"
    set_cantidad_minutos.short_description = "Cantidad de Minutos"
    set_id.short_description = "ID"
    set_id_cliente.short_description = "Cliente"
    set_id_consola.short_description = "N° Consola"
    set_abierto.short_description = "Estado"
    
    form = SesionForm

# Desregistrar el modelo Group
admin.site.unregister(Group)