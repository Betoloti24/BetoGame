from django.db import models
from django.core.validators import MinValueValidator
from datetime import date
"""
    Modelo de Producto
    #* id: numerico(5)
    * nombre: varchar(40)
    * precio_venta: numerico(8,2)
    * cant_invent: numerico(3)
    * tipo_producto: varchar(25) (Check) 
    * f_creacion: date(YYYY-MM-DD)
    ° f_actualizacion: date(YYYY-MM-DD)
"""
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40, null=False)
    precio_venta = models.DecimalField(max_digits=8, decimal_places=2, null=False, validators=[MinValueValidator(0)])
    cant_invent = models.IntegerField(null=False,  validators=[MinValueValidator(0)])
    
    TIPOS_PRODUCTO = [
        ('bebida', 'Bebida'),
        ('dulce', 'Dulce'),
        ('salado', 'Salado'),
        ('otro', 'Otro'),
    ]
    tipo_producto = models.CharField(max_length=25, choices=TIPOS_PRODUCTO, null=False)
    
    f_creacion = models.DateField(auto_now_add=True, null=False)
    f_actualizacion = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-f_creacion']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def save(self, *args, **kwargs):
        # Actualizar la fecha de actualización al día actual
        self.f_actualizacion = date.today()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.nombre}"

"""
    Modelo de Historico de Precios
    #* id: numerico(5)
    * id_producto: numerico(5)
    * precio: numerico(8,2)
    * fh_registro: datetime(YYYY-MM-DDTHH:MM:SS) 
    * vigente: booleano
"""
class HistoricoPrecios(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=8, decimal_places=2, null=False, validators=[MinValueValidator(0)])
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
    * costo: numerico(8,2)
    * cant_ingresada: numerico(5)
    * id_producto: numerico(5)
    * fh_registro: datetime(YYYY-MM-DDTHH:MM:SS) 
    * tipo_entrada: varchar(30) (Check)
    ° proveedor: varchar(30)
"""
class Entrada(models.Model):
    id = models.AutoField(primary_key=True)
    costo = models.DecimalField(max_digits=8, decimal_places=2, null=False, validators=[MinValueValidator(0)])
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    fh_registro = models.DateTimeField(auto_now_add=True, null=False)
    
    TIPOS_ENTRADA = [
        ('compra', 'Comprado'),
        ('produccion', 'Producido'),
    ]
    tipo_entrada = models.CharField(max_length=30, choices=TIPOS_ENTRADA, null=False)
    cant_ingresada = models.IntegerField(null=False,  validators=[MinValueValidator(0)])
    proveedor = models.CharField(max_length=30, null=True, blank=True)
    class Meta:
        ordering = ['-fh_registro']
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self) -> str:
        return f"{self.cant_ingresada} unidades de {self.id_producto.nombre}"
