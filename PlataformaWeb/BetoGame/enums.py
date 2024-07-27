from django.db import models

class MetodoPago(models.TextChoices):
    EFECTIVODOLAR = 'efectivodolar', 'Efectivo $'
    EFECTIVOBS = 'efectivobs', 'Efectivo Bs'
    TARJETA = 'tarjeta', 'Tarjeta'
    PAGO_MOVIL = 'pago_movil', 'Pago Móvil'
