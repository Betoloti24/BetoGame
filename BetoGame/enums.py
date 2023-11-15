from django.db import models

class MetodoPago(models.TextChoices):
    EFECTIVODOLAR = 'efectivodolar', 'EfectivoDolar'
    EFECTIVOBS = 'efectivobs', 'EfectivoBs'
    TARJETA = 'tarjeta', 'Tarjeta'
    PAGO_MOVIL = 'pago_movil', 'Pago Móvil'