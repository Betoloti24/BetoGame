from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from Inventario.models import Producto, HistoricoPrecios, Entrada
from Inventario.form import EntradaForm, ProductoForm, HistoricoPreciosForm

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'set_nombre', 'set_tipo_producto', 'set_precio_venta', 'set_precio_venta_dolar', 'set_precio_compra', 'set_precio_compra_dolar', 'set_cant_invent', 'set_fecha_creacion', 'set_fecha_actualizacion')
    list_filter = ('tipo_producto',)
    search_fields = ('nombre',)
    date_hierarchy = 'f_creacion'
    
    readonly_fields = ('f_actualizacion','precio_compra','cant_invent', 'precio_venta_dolar', 'precio_compra_dolar')

    # Formateo de los campos
    def set_fecha_creacion(self, obj):
        return obj.f_creacion.strftime('%Y-%m-%d')
    def set_fecha_actualizacion(self, obj):
        if obj.f_actualizacion:
            return obj.f_actualizacion.strftime('%Y-%m-%d')
        return ""
    def set_precio_venta(self, obj):
        return f"{obj.precio_venta:.2f}Bs"
    def set_precio_compra(self, obj):
        return f"{obj.precio_compra:.2f}Bs" if obj.precio_compra else f"{0.0}Bs"
    def set_precio_venta_dolar(self, obj):
        return f"{obj.precio_venta_dolar:.2f}$"
    def set_precio_compra_dolar(self, obj):
        return f"{obj.precio_compra_dolar:.2f}$" if obj.precio_compra_dolar else f"{0.0}$"
    def set_cant_invent(self, obj):
        return f"{obj.cant_invent}"
    def set_tipo_producto(self, obj):
        tipos = {
            'bebida': 'Bebida',
            'dulce': 'Dulce',
            'salado': 'Salado',
            'otro': 'Otro',
        }
        return f"{tipos.get(obj.tipo_producto, obj.tipo_producto)}"
    def set_nombre(self, obj):
        return f"{obj.nombre}"
    
    # Asignacion de los nombres a los campos
    set_fecha_creacion.short_description = 'Fecha de Creación'
    set_fecha_actualizacion.short_description = 'Fecha de Actualización'
    set_precio_venta.short_description = 'Precio de Venta (Bs)'
    set_precio_compra.short_description = 'Precio de Compra (Bs)'
    set_precio_venta_dolar.short_description = 'Precio de Venta ($)'
    set_precio_compra_dolar.short_description = 'Precio de Compra ($)'
    set_cant_invent.short_description = 'Cantidad en Inventario'
    set_tipo_producto.short_description = 'Tipo de Producto'
    set_nombre.short_description = 'Nombre'

    form = ProductoForm

@admin.register(HistoricoPrecios)
class HistoricoPreciosAdmin(admin.ModelAdmin):
    list_display = ('id', 'set_id_producto', 'set_precio', 'set_precio_dolar', 'set_fecha_creacion', 'set_vigente')
    list_filter = ('vigente',)
    date_hierarchy = 'fh_registro'
    ordering = ('-fh_registro',)
    readonly_fields = ('vigente',)

    # Formateo de los campos
    def set_fecha_creacion(self, obj):
        return obj.fh_registro.strftime('%Y-%m-%d')
    def set_precio(self, obj):
        return f"{obj.precio:.2f}Bs"
    def set_precio_dolar(self, obj):
        return f"{obj.precio_dolar:.2f}$"
    def set_vigente(self, obj):
        return f"Si" if obj.vigente else "No"
    def set_id_producto(self, obj):
        return f"{obj.id_producto.nombre}"
    
    # Asignacion de los nombres a los campos
    set_fecha_creacion.short_description = 'Fecha de Creación'
    set_precio.short_description = 'Precio (Bs)'
    set_precio_dolar.short_description = 'Precio ($)'
    set_vigente.short_description = '¿Vigente?'
    set_id_producto.short_description = 'Producto'

    form = HistoricoPreciosForm

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('id', 'set_id_producto', 'set_tipo_entrada', 'set_costo_punidad',  'set_costo_punidad_dolar', 'set_costo_mercancia', 'set_costo_mercancia_dolar', 'set_costo_envio', 'set_costo_envio_dolar', 'set_cant_ingresada', 'set_fecha_creacion')
    list_filter = ('tipo_entrada',)
    date_hierarchy = 'fh_registro'
    ordering = ('-fh_registro',)
    readonly_fields = ('costo_punidad', 'costo_punidad_dolar', 'costo_mercancia_dolar', 'costo_envio_dolar')

    # Ajustar el articulo del mensaje del administardor
    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        # Personalizar el mensaje de éxito según el modelo
        if 'Sesion' in message:
            message = format_html("La Entrada '{}' se cambió correctamente.", message.split('</a>')[0].split('">')[-1])

        super().message_user(request, message, level, extra_tags, fail_silently)

    # Control de errores
    def save_model(self, request, obj, form, change):
        producto = Producto.objects.get(id=obj.id_producto.id)
        super().save_model(request, obj, form, change)
        # Verificamos si el precio de compra es mayor al de venta
        if (obj.costo_punidad >= producto.precio_venta):
            self.message_user(request, f"La entrada generada tuvo un coste por unidad superior al precio de venta del producto {producto.nombre}. Actualice el precio de venta del producto.", level='warning')

    # Formateo de los campos
    def set_fecha_creacion(self, obj):
        return obj.fh_registro.strftime('%Y-%m-%d')
    def set_id_producto(self, obj):
        return f"{obj.id_producto.nombre}"
    def set_tipo_entrada(self, obj):
        if obj.tipo_entrada == 'compra':
            return 'Compra'
        if obj.tipo_entrada == 'produccion':
            return 'Producción'
        return f"{obj.tipo_entrada}"
    def set_costo_punidad(self, obj):
        return f"{obj.costo_punidad:.2f}Bs"
    def set_costo_mercancia(self, obj):
        return f"{obj.costo_mercancia:.2f}Bs"
    def set_costo_envio(self, obj):
        return f"{obj.costo_envio:.2f}Bs"
    def set_costo_punidad_dolar(self, obj):
        return f"{obj.costo_punidad_dolar:.2f}$"
    def set_costo_mercancia_dolar(self, obj):
        return f"{obj.costo_mercancia_dolar:.2f}$"
    def set_costo_envio_dolar(self, obj):
        return f"{obj.costo_envio_dolar:.2f}$"
    def set_cant_ingresada(self, obj):
        return f"{obj.cant_ingresada} unidades"
    
    # Asignacion de los nombres a los campos
    set_fecha_creacion.short_description = 'Fecha de Creación'
    set_id_producto.short_description = 'Producto'
    set_tipo_entrada.short_description = 'Tipo de Entrada'
    set_costo_punidad.short_description = 'Costo por Unidad (Bs)'
    set_costo_mercancia.short_description = 'Costo de Mercancia (Bs)'
    set_costo_envio.short_description = 'Costo de Envio (Bs)'
    set_costo_punidad_dolar.short_description = 'Costo por Unidad ($)'
    set_costo_mercancia_dolar.short_description = 'Costo de Mercancia ($)'
    set_costo_envio_dolar.short_description = 'Costo de Envio ($)'
    set_cant_ingresada.short_description = 'Cantidad Ingresada'

    form = EntradaForm