from django.contrib import admin
from .models import Producto
from django.contrib import messages
from django.utils.html import format_html
from .models import Producto, HistoricoPrecios, Entrada
from .form import EntradaForm

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio_venta', 'precio_compra', 'cant_invent', 'tipo_producto', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('tipo_producto',)
    search_fields = ('nombre',)
    date_hierarchy = 'f_creacion'
    
    readonly_fields = ('f_actualizacion','precio_compra','cant_invent')

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
    list_display = ('id', 'id_producto', 'costo_punidad', 'cant_ingresada', 'costo_mercancia', 'costo_envio', 'tipo_entrada', 'fecha_creacion')
    list_filter = ('tipo_entrada',)
    date_hierarchy = 'fh_registro'
    ordering = ('-fh_registro',)
    readonly_fields = ('costo_punidad',)
    form = EntradaForm

    # Ajustar el articulo del mensaje del administardor
    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        # Personalizar el mensaje de éxito según el modelo
        if 'Sesion' in message:
            message = format_html("La Entrada '{}' se cambió correctamente.", message.split('</a>')[0].split('">')[-1])

        super().message_user(request, message, level, extra_tags, fail_silently)

    # Formateo de las fechas
    def fecha_creacion(self, obj):
        return obj.fh_registro.strftime('%Y-%m-%d')
    
    # Control de errores
    def save_model(self, request, obj, form, change):
        producto = Producto.objects.get(id=obj.id_producto.id)
        super().save_model(request, obj, form, change)
        # Verificamos si el precio de compra es mayor al de venta
        if (obj.costo_punidad >= producto.precio_venta):
            self.message_user(request, f"La entrada generada tuvo un coste por unidad superior al precio de venta del producto {producto.nombre}. Actualice el precio de venta del producto.", level='warning')
        