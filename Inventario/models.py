from collections.abc import Iterable
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import date
"""
    Modelo de Producto
    #* id: numerico(5)
    * nombre: varchar(20)
    * precio_venta: numerico(10,2)
    * precio_compra: numerico(10,2)
    * cant_invent: numerico(3)
    * tipo_producto: varchar(6) (Check) 
    * f_creacion: date(YYYY-MM-DD)
    ° f_actualizacion: date(YYYY-MM-DD)
"""
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, null=False)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.0, validators=[MinValueValidator(0)])
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0, validators=[MinValueValidator(0)])
    cant_invent = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])
    
    TIPOS_PRODUCTO = [
        ('bebida', 'Bebida'),
        ('dulce', 'Dulce'),
        ('salado', 'Salado'),
        ('otro', 'Otro'),
    ]
    tipo_producto = models.CharField(max_length=6, choices=TIPOS_PRODUCTO, null=False)
    
    f_creacion = models.DateField(auto_now_add=True, null=False)
    f_actualizacion = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-f_creacion']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def save(self, *args, **kwargs):
        # Actualizar la fecha de actualización al día actual
        self.f_actualizacion = timezone.now()
        
        # Guardamos el producto
        super().save(*args, **kwargs)

        ## CREAR REGISTRO DE PRECIO
        # Verifica si ya hay un historico vigente y lo marca como no vigente
        historico_vigente = HistoricoPrecios.objects.filter(id_producto=self, vigente=True).first()
        if historico_vigente and self.precio_venta != historico_vigente.precio:
            historico_vigente.vigente = False
            historico_vigente.save()
        
            # Crea un nuevo registro en el historico
            nuevo_historico = HistoricoPrecios(id_producto=self, precio=self.precio_venta, vigente=True)
            nuevo_historico.save()
        elif not historico_vigente:
            # Crea un nuevo registro en el historico
            nuevo_historico = HistoricoPrecios(id_producto=self, precio=self.precio_venta, vigente=True)
            nuevo_historico.save()

    def __str__(self) -> str:
        return f"{self.nombre}"

"""
    Modelo de Historico de Precios
    #* id: numerico(5)
    * id_producto: numerico(5)
    * precio: numerico(10,2)
    * fh_registro: datetime(YYYY-MM-DDTHH:MM:SS) 
    * vigente: booleano
"""
class HistoricoPrecios(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False, validators=[MinValueValidator(1)])
    fh_registro = models.DateTimeField(auto_now_add=True, null=False)
    vigente = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fh_registro']
        verbose_name = 'Historico de Precios'
        verbose_name_plural = 'Historicos de Precios'
    
    def __str__(self) -> str:
        return f"Con precio vigente de {self.precio}Bs.D del producto {self.id_producto.nombre}"

"""
    Modelo de Entrada
    #* id: numerico(5)
    * costo_punidad: numerico(10,2)
    * costo_mercancia: numerico(10,2)
    * costo_envio: numerico(10,2)
    * cant_ingresada: numerico(5)
    * id_producto: numerico(5)
    * fh_registro: datetime(YYYY-MM-DDTHH:MM:SS) 
    * tipo_entrada: varchar(10) (Check)
    ° proveedor: varchar(20)
"""
class Entrada(models.Model):
    id = models.AutoField(primary_key=True)
    costo_punidad = models.DecimalField(max_digits=10, decimal_places=2, null=False, validators=[MinValueValidator(1)])
    costo_mercancia = models.DecimalField(max_digits=10, decimal_places=2, null=False, validators=[MinValueValidator(1)])
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0, validators=[MinValueValidator(0)])
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    fh_registro = models.DateTimeField(auto_now_add=True, null=False)
    
    TIPOS_ENTRADA = [
        ('compra', 'Comprado'),
        ('produccion', 'Producido'),
    ]
    tipo_entrada = models.CharField(max_length=10, choices=TIPOS_ENTRADA, null=False)
    cant_ingresada = models.IntegerField(null=False,  validators=[MinValueValidator(1)])
    proveedor = models.CharField(max_length=20, null=True, blank=True)
    
    class Meta:
        ordering = ['-fh_registro']
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def save(self, *args, **kwargs) -> None:
        ## Aumentamos la existencia del producto
        producto = Producto.objects.get(id=self.id_producto.id)
        producto.cant_invent += self.cant_ingresada

        ## Calculamos el precio por unidad
        costo_compra = (self.costo_envio + self.costo_mercancia)/self.cant_ingresada
        self.costo_punidad = costo_compra

        ## Actualizamos el precio de compra
        producto.precio_compra = self.costo_punidad
        producto.save()
        super().save(self, *args, **kwargs)

    def __str__(self) -> str:
        return f"{self.cant_ingresada} unidades de {self.id_producto.nombre}"
