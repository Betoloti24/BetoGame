from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError
from BetoGame.enums import MetodoPago
from datetime import date, datetime, timedelta
from decimal import Decimal

## RESTRICCIONES DE VERIFICACION
def consola_ocupada(value):
    consola = Consola.objects.filter(numero=value).first()
    if consola.ocupada:
        raise ValidationError("La consola seleccionada está ocupada")
    
def existencia_producto(producto, cantidad):
    if not producto.cant_invent or producto.cant_invent < cantidad:
        raise ValidationError("Cantidad no valida. Existencia del producto insuficiente.")

"""
    Modelo de Cliente
    #* ci: numerico(8)
    * nombre: varchar(30)
    * apellido: varchar(30)
    * genero: varchar(1) (Check)
    * f_nacimiento: date(YYYY-MM-DD)
    * ubicacion: varchar(50)
    * telefono: varchar(11)
    * correo: varchar(50)
    * minutos_favor: numerico(3)
    * f_creacion: date(YYYY-MM-DD)
    ° f_actualizacion: date(YYYY-MM-DD)
"""
class Cliente(models.Model):
    ci = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=30, null=False)
    apellido = models.CharField(max_length=30, null=False)
    
    GENEROS = [
        ('M', 'Masculino'),
        ('F', 'Femenino')
    ]
    genero = models.CharField(max_length=1, choices=GENEROS, null=False)
    f_nacimiento = models.DateField(null=False)
    ubicacion = models.CharField(max_length=50, null=False)
    telefono = models.CharField(max_length=11, null=False)
    correo = models.EmailField(max_length=50, null=False, unique=True)
    minutos_favor = models.PositiveIntegerField(null=False, validators=[MinValueValidator(0)], blank=True, default=0)
    f_creacion = models.DateField(auto_now_add=True, null=False)
    f_actualizacion = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-f_creacion']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    # Actualizar la fecha de actualización al día actual
    def save(self, *args, **kwargs):
        self.f_actualizacion = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"

"""
    Modelo de Compra
    #* id: numerico(5)
    * id_producto: numerico(3)
    * id_cliente: numerico(8)
    * fh_compra: datetime(YYYY-MM-DD HH:MM:SS) 
    * cantidad: numerico(2)
    * monto: numerico(5,2)
"""
class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Inventario.Producto', on_delete=models.CASCADE)
    id_cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    id_cuenta = models.ForeignKey('Caja.Cuenta', null=True, blank=True, on_delete=models.CASCADE) 
    fh_venta = models.DateTimeField(auto_now_add=True, null=False)
    cantidad = models.IntegerField(null=False, validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['-fh_venta']
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    # realizamos las validaciones
    def clean(self):
        existencia_producto(self.id_producto, self.cantidad)
        super().clean()

    # guardar venta
    def save(self, *args, **kwargs):
        from Caja.models import Cuenta, Variable
        
        ## DISMINUIR EXISTENCIA
        producto = self.id_producto
        cantidad_compra = self.cantidad
        print(producto)
        # Validamos la existencia
        
        producto.cant_invent -= cantidad_compra
        producto.save()

        # Asignamos la cuenta
        monto_dolar = (producto.precio_venta * cantidad_compra) 
        cuenta_cliente = Cuenta.objects.filter(id_cliente=self.id_cliente, fh_pago=None).first()
        if not cuenta_cliente:
            cuenta_cliente = Cuenta(id_cliente = self.id_cliente, monto_deberdolar=monto_dolar)
        else:
            cuenta_cliente.monto_deberdolar += monto_dolar
        cuenta_cliente.save()
        self.id_cuenta = cuenta_cliente

        # Guardar el registro
        super().save(self, *args, **kwargs)

    def __str__(self) -> str:
        return f"{self.cantidad} unidades de {self.id_producto.nombre}"

"""
    Modelo de Juego
    #* id: numerico(5)
    * nombre: varchar(30)
    * f_compra: date(YYY-MM-DD)
    * generos: varchar(10) (Check)
    * tipo: varchar(7) (Check)
    * precio_compra: numerico(5,2)
    * cantidad: numerico(2)
"""
class Juego(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    f_compra = models.DateField(auto_now_add=True, null=False)
    precio_compra = models.DecimalField(max_digits=8, decimal_places=2, null=False, validators=[MinValueValidator(1)])
    cantidad = models.PositiveIntegerField(null=False)
    
    GENERO_JUEGO = [
        ('accion', 'Acción'),
        ('aventura', 'Aventura'),
        ('deportes', 'Deportes'),
        ('estrategia', 'Estrategia'),
        ('otros', 'Otros'),
    ]
    genero = models.CharField(max_length=10, choices=GENERO_JUEGO, null=False)

    TIPO_JUEGO = [
        ('fisico', 'Físico'),
        ('digital', 'Digital')
    ]
    tipo = models.CharField(max_length=7, choices=TIPO_JUEGO, null=False)
    
    class Meta:
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'

    def __str__(self) -> str:
        return f"{self.nombre}"

"""
    Modelo de Consola
    #* numero: numerico(2)
    * cant_controles: numerico(1)
    * ocupada: boolean
    ° serial: varchar(30)
"""
class Consola(models.Model):
    numero = models.PositiveIntegerField(primary_key=True)
    cant_controles = models.PositiveIntegerField(null=False)
    ocupada = models.BooleanField(default=False)
    juegos_instalados = models.ManyToManyField('Juego')
    serial = models.CharField(max_length=30, null=True, blank=True)
    f_actualizacion = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Consola'
        verbose_name_plural = 'Consolas'
    
    # Actualizar la fecha de actualización al día actual
    def save(self, *args, **kwargs):
        self.f_actualizacion = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Numero {self.numero}"

"""
    Modelo de Sesion
    *# id: nuemrico(5)
    * h_inicio: time(HH:MM:SS) 
    * h_final: time(HH:MM:SS) 
    * f_sesion: date(YYYY-MM-DD)
    * id_cliente: numerico(8) (FK)
    * id_consola: numerico(2) (FK)
    * cant_minutos: numerico(3)
    * cant_personas: numerico(1)
    * abierto: boolean
    ° minutos_regalo: numerico(2)
"""
class Sesion(models.Model):
    id = models.AutoField(primary_key=True)
    h_inicio = models.TimeField(auto_now_add=True, null=False)
    h_final = models.TimeField(null=False)
    f_sesion = models.DateTimeField(auto_now_add=True, null=False)
    id_cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    id_consola = models.ForeignKey('Consola', on_delete=models.CASCADE, validators=[consola_ocupada])
    id_cuenta = models.ForeignKey('Caja.Cuenta', on_delete=models.CASCADE) 
    minutos_regalo = models.PositiveIntegerField(null=False, validators=[MinValueValidator(0)], blank=True, default=0)
    abierto = models.BooleanField(default=True)
    
    cant_minutos = models.PositiveIntegerField(null=False, validators=[MinValueValidator(1)])
    cant_personas = models.PositiveIntegerField(null=False, validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Sesion'
        verbose_name_plural = 'Sesiones'

    def save(self, *args, **kwargs):
        from Caja.models import Cuenta, Variable
        consola = Consola.objects.filter(numero=self.id_consola.numero).first()
        
        # Asigno la hora de finalizacion
        minutos_juego = self.cant_minutos + self.minutos_regalo
        self.h_final = datetime.now() + timedelta(minutes=minutos_juego)

        # Asigno la cuenta del cliente
        cuenta_cliente = Cuenta.objects.filter(id_cliente=self.id_cliente, fh_pago=None).first()
        if not cuenta_cliente:
            nueva_cuenta_cliente = Cuenta(id_cliente=self.id_cliente)
            nueva_cuenta_cliente.save()
            cuenta_cliente = Cuenta.objects.filter(id_cliente=self.id_cliente, fh_pago=None).first()
        
        # Consultamos las variables de referencia
        precio_hora = Variable.objects.filter(id=1).first().convert()
        # Actualizamos los montos de la cuenta
        monto_pagar_dolares = Decimal(str((self.cant_minutos/60)*precio_hora))
        cuenta_cliente.monto_deberdolar += monto_pagar_dolares
        cuenta_cliente.save()
        self.id_cuenta = cuenta_cliente

        # Actualizamos la ocupacion de la consola
        consola.ocupada = True
        consola.save()
        super().save(*args, **kwargs)   
        

    def __str__(self) -> str:
        return f"Con inicio {self.h_inicio} hasta las {self.h_final}"
