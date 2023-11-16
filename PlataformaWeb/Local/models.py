from django.db import models
from django.core.validators import MinValueValidator
from BetoGame.enums import MetodoPago
from datetime import date, datetime

"""
    Modelo de Cliente
    #* ci: numerico(10)
    * nombre: varchar(30)
    * apellido: varchar(30)
    * genero: varchar(10) (Check)
    * f_nacimiento: date(YYYY-MM-DD)
    * ubicacion: varchar(100)
    * telefono: varchar(15)
    * correo: varchar(50)
    * f_creacion: date(YYYY-MM-DD)
    ° f_actualizacion: date(YYYY-MM-DD)
"""
class Cliente(models.Model):
    ci = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    apellido = models.CharField(max_length=30, null=False)
    
    GENEROS = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino')
    ]
    genero = models.CharField(max_length=10, choices=GENEROS, null=False)
    f_nacimiento = models.DateField(null=False)
    ubicacion = models.CharField(max_length=100, null=False)
    telefono = models.CharField(max_length=15, null=False)
    correo = models.EmailField(max_length=50, null=False, unique=True)
    f_creacion = models.DateField(auto_now_add=True, null=False)
    f_actualizacion = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-f_creacion']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    # Actualizar la fecha de actualización al día actual
    def save(self, *args, **kwargs):
        self.f_actualizacion = date.today()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"

"""
    Modelo de Compra
    #* id: numerico(5)
    * id_producto: numerico(5)
    * id_cliente: numerico(10)
    * met_pago: varchar(15) (Check)
    * fh_compra: datetime(YYYY-MM-DDTHH:MM:SS) 
    * cantidad: numerico(5)
    * monto: numerico(8,2)
"""
class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Inventario.Producto', on_delete=models.CASCADE)
    id_cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    met_pago = models.CharField(max_length=15, choices=MetodoPago.choices, null=False)
    fh_compra = models.DateTimeField(auto_now_add=True, null=False)
    cantidad = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    monto = models.DecimalField(max_digits=8, decimal_places=2, null=False, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['-fh_compra']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
    
    def __str__(self) -> str:
        return f"{self.cantidad} unidades de {self.id_producto.nombre}"

"""
    Modelo de Juego
    #* id: numerico(5)
    * nombre: varchar(30)
    * f_compra: date(YYY-MM-DD)
    * generos: varchar(50)
    * precio_compra: date(YYYY-MM-DD)
    * cantidad: numerico(2)
    * tipo: varchar(20) (Check)
    * empresa: varchar(50)
"""
class Juego(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    f_compra = models.DateField(auto_now_add=True, null=False)
    precio_compra = models.DecimalField(max_digits=8, decimal_places=2, null=False, validators=[MinValueValidator(0)])
    cantidad = models.PositiveIntegerField(null=False)
    
    GENERO_JUEGO = [
        ('accion', 'Acción'),
        ('aventura', 'Aventura'),
        ('deportes', 'Deportes'),
        ('estrategia', 'Estrategia'),
        ('otros', 'Otros'),
    ]
    genero = models.CharField(max_length=20, choices=GENERO_JUEGO, null=False)

    class Meta:
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'

    def __str__(self) -> str:
        return f"{self.nombre}"

"""
    Modelo de Consola
    #* numero: numerico(2)
    * cant_controles: numerico(2)
    ° serial: varchar(30)
"""
class Consola(models.Model):
    numero = models.PositiveIntegerField(primary_key=True)
    cant_controles = models.PositiveIntegerField(null=False)
    serial = models.CharField(max_length=30, null=True, blank=True)
    
    juegos_instalados = models.ManyToManyField('Juego')
    f_actualizacion = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Consola'
        verbose_name_plural = 'Consolas'
    
    # Actualizar la fecha de actualización al día actual
    def save(self, *args, **kwargs):
        self.f_actualizacion = date.today()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Numero {self.numero}"

"""
    Modelo de Sesion
    *# id: nuemrico(5)
    * fh_inicio: datetime(YYYY-MM-DDTHH:MM:SS) 
    * fh_final: datetime(YYYY-MM-DDTHH:MM:SS) 
    * id_cliente: numerico(10) (FK)
    * id_consola: numerico(2) (FK)
    * met_pago: varchar(15) (Check)
    * cant_horas: numerico(1,5)
    * cant_personas: numerico(2)
"""
class Sesion(models.Model):
    id = models.AutoField(primary_key=True)
    h_inicio = models.TimeField(null=False)
    h_final = models.TimeField(null=False)
    f_sesion = models.DateTimeField(auto_now_add=True, null=False)
    id_cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    id_consola = models.ForeignKey('Consola', on_delete=models.CASCADE)
    
    met_pago = models.CharField(max_length=15, choices=MetodoPago.choices, null=False)
    
    cant_horas = models.DecimalField(max_digits=5, decimal_places=1, null=False, validators=[MinValueValidator(0)])
    cant_personas = models.PositiveIntegerField(null=False, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Sesion'
        verbose_name_plural = 'Sesiones'

    def save(self, *args, **kwargs):
        self.h_final = datetime.now().time()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Con inicio {self.h_inicio} hasta las {self.h_final}"