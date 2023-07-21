from django.db import models


class Train(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Поезд',
    )
    travel_time = models.PositiveSmallIntegerField(
        verbose_name='Время в пути'
    )
    from_city = models.ForeignKey(
        'cities.City',
        on_delete=models.CASCADE,
        related_name='from_city_set',
        verbose_name='Из какого города'
    )
    to_city = models.ForeignKey(
        'cities.City',
        on_delete=models.CASCADE,
        related_name='to_city_set',
        verbose_name='В какой город'
    )
    
    def __str__(self):
        return f"Поезд {self.name} из {self.from_city} в {self.to_city}"
    
    class Meta:
        verbose_name = 'поезд'
        verbose_name_plural = 'поезда'
        ordering = ['travel_time']
