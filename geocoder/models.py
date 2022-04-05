from django.db import models
from django.utils import timezone


class Place(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=100,
        blank=True,
        unique=True
    )
    lng = models.FloatField('Долгота', null=True)
    lat = models.FloatField('Широта', null=True)
    registered_at = models.DateTimeField(
        default=timezone.now,
        db_index=True
    )

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return f'{self.address}: {self.created_at}'

