from typing import Any
from django.db import models
from django.utils import timezone
from django.forms import ValidationError
from django.db.models import Q
from datetime import date, datetime, timedelta
from BetoGame.enums import MetodoPago
from functools import reduce
from decimal import Decimal
from django.core.validators import MinValueValidator

## REGLAS DE VERIFICACION
def monto_pagar(cuenta, monto_bs):
    if cuenta.monto_deber < monto_bs:
        raise ValidationError("El monto a pagar excede la deuda.")

"""
    Modelo de Cuenta:
    #* id: numerico(5)
    * id_cliente: numerico(8) (FK)
    * compras: numerico(5) (FK)
    * sesiones: numerico(5) (FK) 
    * monto_deber: numerico(10, 2)
    * monto_pagado: numerico(10, 2)
    * fh_creacion: datatime(YYYY-MM-DD HH:MM:SS)
    ° fh_pago: datatime(YYYY-MM-DD HH:MM:SS)
"""
class Cuenta(models.Model):
    id = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey('Local.Cliente', on_delete=models.CASCADE)
    monto_deber = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    monto_deber_dolar = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    monto_pagado_dolar = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    fh_creacion = models.DateTimeField(auto_now_add=True, null=False)
    fh_ultimo_pago = models.DateTimeField(null=True, blank=True)
    fh_pago = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Cuenta de {self.monto_deber}Bs ({self.monto_deber_dolar}$) para el Cliente: {self.id_cliente.nombre} {self.id_cliente.apellido}'
    
    def ajustar_deuda(self, cambio):
        self.monto_deber = self.monto_deber_dolar*cambio
        self.save()


"""
    Modelo de Pago
    #* id: numerico(5)
    * id_cuenta: numerico/(5)
    * met_pago: varchar(10) (Check)
    * monto: numerico(10,2)
    * fh_pago: datetime(YYYY-MM-DD HH:MM:SS)
"""
class Pago(models.Model):
    id = models.AutoField(primary_key=True)
    id_cuenta = models.ForeignKey('Cuenta', on_delete=models.CASCADE)
    met_pago = models.CharField(max_length=13, choices=MetodoPago.choices)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(1)])
    monto_dolar = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(1)])
    fh_pago = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    # validaciones
    def clean(self):
        monto_pagar(self.id_cuenta, self.monto)
        super().clean()

    # guardamos
    def save(self, *args, **kwargs):
        from Caja.models import Variable
        cambio = Variable.objects.filter(id=2).first().convert()
        self.monto_dolar = self.monto/cambio
        super().save(*args, **kwargs)
        # consultamos el cambio del dia
        # actualizamos la deuda y lo pagado de la cuenta
        cuenta = Cuenta.objects.filter(id=self.id_cuenta.id).first()
        cuenta.monto_deber -= self.monto
        cuenta.monto_deber_dolar -= self.monto/cambio
        cuenta.monto_pagado += self.monto
        cuenta.monto_pagado_dolar += self.monto/cambio

        cuenta.fh_ultimo_pago = self.fh_pago
        if (cuenta.monto_deber == 0):
            cuenta.fh_pago = timezone.now()
        # import pdb; pdb.set_trace()
        cuenta.save()


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
    * total_minutos: numerico(5) 
    * total_jugadores: numerico(2)
    * totalbs_costoent: numerico(8,2)
    * totaldolar_costoent: numerico(5,2)
    * fh_cierre: datetime(YYYY-MM-DD HH:MM:SS) 
"""
class Cierre(models.Model):
    id = models.AutoField(primary_key=True)
    fh_cierre = models.DateField(unique=True)
    totalbs_ingreso = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    totaldolar_ingreso = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    totalbs_fianza = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    totaldolar_fianza = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    totalbs_costoent = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    totaldolar_costoent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total_jugadores = models.DecimalField(max_digits=3, decimal_places=0, default=0.0)
    total_horas = models.DecimalField(max_digits=3, decimal_places=0, default=0.0)
    total_minutos = models.DecimalField(max_digits=5, decimal_places=0, default=0.0)

    class Meta:
        verbose_name = 'Cierre'
        verbose_name_plural = 'Cierres'

    def save(self, *args, **kwargs):
        from Local.models import Sesion
        from Inventario.models import Entrada
        fecha_inicio = datetime(year=self.fh_cierre.year, month=self.fh_cierre.month, day=self.fh_cierre.day, hour=0, minute=0, second=0)
        fecha_final = datetime(year=self.fh_cierre.year, month=self.fh_cierre.month, day=self.fh_cierre.day, hour=23, minute=59, second=59)
        cambio = Variable.objects.filter(id=2).first().convert()
        
        # calcular los ingresos
        pagos = Pago.objects.filter(fh_pago__range=(fecha_inicio, fecha_final))
        if pagos:
            ingresos = sum([x.monto for x in pagos])
        else:
            ingresos = 0
        self.totaldolar_ingreso = ingresos/cambio
        self.totalbs_ingreso = ingresos

        # calcular fiado
        cuentas = Cuenta.objects.filter(Q(fh_ultimo_pago=None) | Q(fh_ultimo_pago__lte=fecha_final))
        if cuentas:
            fiado = sum([x.monto_deber for x in cuentas])
        else:
            fiado = 0
        self.totaldolar_fianza = fiado/cambio
        self.totalbs_fianza = fiado

        # calcular cantidad de horas y jugadores
        sesiones = Sesion.objects.filter(f_sesion__range=(fecha_inicio, fecha_final))
        if sesiones:
            cant_horas = sum([(x.minutos_regalo+x.cant_minutos)/60 for x in sesiones])
            cant_minutos = sum([x.minutos_regalo+x.cant_minutos for x in sesiones])
            cant_jugadores = sum([x.cant_personas for x in sesiones])
        else:
            cant_horas = 0
            cant_minutos = 0
            cant_jugadores = 0
        self.total_horas = cant_horas
        self.total_minutos = cant_minutos
        self.total_jugadores = cant_jugadores

        # calcular costo de entradas
        entradas = Entrada.objects.filter(fh_registro__range=(fecha_inicio, fecha_final))
        if entradas:
            costo_entradas = sum([x.costo_mercancia + x.costo_envio for x in entradas])
        else:
            costo_entradas = 0
        self.totaldolar_costoent = costo_entradas/cambio
        self.totalbs_costoent = costo_entradas
        super().save(*args, **kwargs)

    def __str__(self):
        return f'A fecha de {self.fh_cierre}'

"""
    Modelo de Variables:
    #* id: numerico(2)
    * nombre: varchar(30)
    * valor: varchar(15) 
    * tipo_dato: varchar(10) (Check)
    * fh_actualizacion: datetime(YYYY-MM-DD HH:MM:SS) 
"""

class VariableManager(models.Manager):
    def create(self, nombre, valor, tipo_dato, **extra_fields):
        # Verificar que el tipo de dato es válido antes de la creación
        if tipo_dato not in dict(Variable.TIPO_DATO):
            raise ValueError("Tipo de dato no válido")
        
        # Crear el objeto utilizando el método `create` del padre
        variable = super().create(
            nombre=nombre,
            valor=valor,
            tipo_dato=tipo_dato,
            fh_actualizacion=timezone.now(),
            **extra_fields
        )
        # Aquí puedes agregar lógica adicional que se ejecuta después de guardar el objeto
        HistoricoValores.objects.create(id_variable=variable, valor=variable.valor)
        
        return variable
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
    # objects = VariableManager()
    class Meta:
        verbose_name = 'Variable'
        verbose_name_plural = 'Variables'

    def save(self, *args, **kwargs):
        # Actualizar la fecha de actualización al día actual
        self.fh_actualizacion = timezone.now()
        
        # Guardamos
        super().save(*args, **kwargs)
        
        # Generamos un historico de valores si se actualiza el registro
        reg_vigente = HistoricoValores.objects.filter(id_variable=self, vigente=True).first()
        if (not reg_vigente or reg_vigente.valor != self.valor):
            # Verifica si ya hay un historico vigente y lo marca como no vigente
            historico_vigente = HistoricoValores.objects.filter(id_variable=self, vigente=True).first()
            if historico_vigente:
                historico_vigente.vigente = False
                historico_vigente.save()

            # Crea un nuevo registro en el historico
            nuevo_historico = HistoricoValores(id_variable=self, valor=self.valor, vigente=True)
            nuevo_historico.save()

            # validamos si estamos actualizando el tipo de cambio
            if self.id == 2:
                # realizamos un ajuste en los precios y deudas en $
                ## deudas
                cuentas = Cuenta.objects.filter(fh_pago=None)
                for cuenta in cuentas: cuenta.ajustar_deuda(self.convert())

                ## precios
                from Inventario.models import Producto
                productos = Producto.objects.all()
                for producto in productos: producto.ajustar_precio(self.convert())
                    


    def convert(self):
        if self.tipo_dato == 'Entero':
            return int(self.valor)
        elif self.tipo_dato == 'Decimal':
            return Decimal(self.valor)   
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
