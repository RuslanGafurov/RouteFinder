from django.db import models


class Route(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Маршрут',
    )
    route_travel_time = models.PositiveSmallIntegerField(
        verbose_name='Общее время в пути'
    )
    from_city = models.ForeignKey(
        'cities.City',
        on_delete=models.CASCADE,
        related_name='route_from_city_set',
        verbose_name='Из какого города'
    )
    to_city = models.ForeignKey(
        'cities.City',
        on_delete=models.CASCADE,
        related_name='route_to_city_set',
        verbose_name='В какой город'
    )
    trains = models.ManyToManyField(
        'trains.Train',
        verbose_name='Список поездов',
    )
    ids = models.JSONField()

    def __str__(self):
        return f"Маршрут {self.name} из {self.from_city} в {self.to_city}"

    class Meta:
        verbose_name = 'маршрут'
        verbose_name_plural = 'маршруты'
        ordering = ['route_travel_time']
