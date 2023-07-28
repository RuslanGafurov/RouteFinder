from django.core.exceptions import ValidationError
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

    def clean(self):
        # Train check method
        if self.from_city == self.to_city:
            raise ValidationError('Города отправления и прибытия должны быть разными')
        train = Train.objects.filter(
            from_city=self.from_city,
            to_city=self.to_city,
            travel_time=self.travel_time,
        ).exclude(pk=self.pk)
        if train.exists():
            raise ValidationError('Такой поезд уже существует')

    def save(self, *args, **kwargs):
        self.clean()
        super(Train, self).save(*args, **kwargs)
