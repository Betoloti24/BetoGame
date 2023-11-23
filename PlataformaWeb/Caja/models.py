from django.db import models
from datetime import date, datetime, timedelta
from BetoGame.enums import MetodoPago

"""
    Modelo de Cuenta:
    #* id: numerico(5)
    * id_cliente: numerico(8) (FK)
    * compras: numerico(5) (FK)
    * sesiones: numerico(5) (FK) 
    * monto_deberdolar: numerico(5, 2)
    * monto_pagado: numerico(5, 2)
    * fh_creacion: datatime(YYYY-MM-DD HH:MM:SS)
    ° fh_creacion: datatime(YYYY-MM-DD HH:MM:SS)
"""
class Cuenta(models.Model):
    id = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey('Local.Cliente', on_delete=models.CASCADE)
    monto_deberdolar = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    monto_pagado = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    fh_creacion = models.DateTimeField(auto_now_add=True, null=False)
    fh_pago = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Cuenta #{self.id} para el Cliente: {self.id_cliente.nombre} {self.id_cliente.apellido}'

"""
    Modelo de Pago
    #* id: numerico(5)
    * id_cuenta: numerico/(5)
    * met_pago: varchar(10) (Check)
    * montodolar: numerico(5,2)
    * fh_pago: datetime(YYYY-MM-DD HH:MM:SS)
"""
class Pago(models.Model):
    id = models.AutoField(primary_key=True)
    id_cuenta = models.ForeignKey('Cuenta', on_delete=models.CASCADE)
    met_pago = models.CharField(max_length=13, choices=MetodoPago.choices)
    montodolar = models.DecimalField(max_digits=5, decimal_places=2)
    fh_pago = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Pago #{self.id} - Cuenta: {self.id_cuenta.id}'

"""
    Modelo de Cierre:
    #* id: numerico(10)
    * totalbs_ingreso: numerico(8,2)
    * totaldolar_ingreso: numerico(5,2)
    * totalbs_fianza: numerico(8,2)
    * totaldolar_fianza: numerico(5,2)
    * total_horas: numerico(3) 
    * total_jugadores: numerico(2)
    * totalbs_costoent: numerico(8,2)
    * totaldolar_costoent: numerico(5,2)
    * fh_cierre: datetime(YYYY-MM-DD HH:MM:SS) 
"""
class Cierre(models.Model):
    id = models.BigAutoField(primary_key=True)
    totalbs_ingreso = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    totaldolar_ingreso = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    totalbs_fianza = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    totaldolar_fianza = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total_horas = models.DecimalField(max_digits=3, decimal_places=0, default=0.0)
    total_jugadores = models.DecimalField(max_digits=2, decimal_places=0, default=0.0)
    totalbs_costoent = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    totaldolar_costoent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    fh_cierre = models.DateTimeField()

    class Meta:
        verbose_name = 'Cierre'
        verbose_name_plural = 'Cierres'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Cierre #{self.id} a fecha de {self.fh_cierre.date()} {self.fh_cierre.time()}'

"""
    Modelo de Variables:
    #* id: numerico(2)
    * nombre: varchar(30)
    * valor: varchar(15) 
    * tipo_dato: varchar(10) (Check)
    * fh_actualizacion: datetime(YYYY-MM-DD HH:MM:SS) 
"""
class Variable(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    valor = models.CharField(max_length=15)
    TIPO_DATO = [
        ('Entero', 'Entero'),
        ('Decimal', 'Decimal'), 
        ('Texto', 'Texto')
    ]
    tipo_dato = models.CharField(max_length=10, choices=TIPO_DATO)
    fh_actualizacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Variable'
        verbose_name_plural = 'Variables'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def convert(self):
        if self.tipo_dato == 'Entero':
            return int(self.valor)
        elif self.tipo_dato == 'Decimal':
            return float(self.valor)   
        return self.valor

    def __str__(self):
        return f'Variable #{self.id} {self.nombre} con el valor {self.valor}'

"""
    Modelo de Historico de Valores
    #* id: numerico(10)
    * id_variable: numerico(2) (FK)
    * valor: varchar(15)
    * fh_registro: datetime(YYYY-MM-DD HH:MM:SS)
    * vigente: boolean
"""
class HistoricoValores(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_variable = models.ForeignKey('Variable', on_delete=models.CASCADE)
    valor = models.CharField(max_length=15)
    fh_registro = models.DateTimeField(auto_now_add=True, null=False)
    vigente = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Histórico de Valores'
        verbose_name_plural = 'Históricos de Valores'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Histórico #{self.id} de la Variable: {self.id_variable.nombre}'
