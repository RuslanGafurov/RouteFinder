from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from cities.models import City
from common.tests import common_tests
from routes.forms import RouteForm
from routes.services import dfs_paths, get_graph
from trains.models import Train


class AllTestsCase(TestCase):

    def setUp(self) -> None:
        """ Начальные данные для БД """

        self.city_A = City.objects.create(name='A')
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')
        trains_list = [
            Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=9),
            Train(name='t2', from_city=self.city_B, to_city=self.city_D, travel_time=8),
            Train(name='t3', from_city=self.city_A, to_city=self.city_C, travel_time=7),
            Train(name='t4', from_city=self.city_C, to_city=self.city_B, travel_time=6),
            Train(name='t5', from_city=self.city_B, to_city=self.city_E, travel_time=3),
            Train(name='t6', from_city=self.city_B, to_city=self.city_A, travel_time=11),
            Train(name='t7', from_city=self.city_A, to_city=self.city_C, travel_time=10),
            Train(name='t8', from_city=self.city_E, to_city=self.city_D, travel_time=5),
            Train(name='t9', from_city=self.city_D, to_city=self.city_E, travel_time=4),
        ]
        Train.objects.bulk_create(trains_list)

    def test_city_model_duplicate(self):
        """ Тестирование возникновения ошибки при создании дубля города """

        city = City(name='A')
        with self.assertRaises(ValidationError):
            city.full_clean()

    def test_train_model_name_duplicate(self):
        """ Тестирование возникновения ошибки при создании дубля поезда по имени """

        train = Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=9999)
        with self.assertRaises(ValidationError):
            train.full_clean()

    def test_train_model_time_duplicate(self):
        """ Тестирование возникновения ошибки при создании дубля поезда по времени"""

        train = Train(name='asdfghj', from_city=self.city_A, to_city=self.city_B, travel_time=9)
        with self.assertRaises(ValidationError):
            train.full_clean()
        try:
            train.full_clean()
        except ValidationError as err:
            self.assertEqual({'__all__': ['Такой поезд уже существует']}, err.message_dict)
            self.assertIn('Такой поезд уже существует', err.messages)

    # Проверка используемых шаблонов и функций
    def test_home_view(self):
        path = reverse('home')
        response = self.client.get(path)

        common_tests(self, response, 'home.html')

    def test_find_all_routes(self):
        """ Тестирование работоспособности функций построения графа и поиска маршрута """

        trains = Train.objects.all()
        graph = get_graph(trains)
        all_routes = list(dfs_paths(graph, self.city_A.id, self.city_E.id))
        self.assertEqual(len(all_routes), 4)

    def test_valid_route_form(self):
        """ Тестирование формы поиска маршрута на валидность """

        data = {
            'from_city': self.city_A.id,
            'to_city': self.city_B.id,
            'cities': [self.city_E.id, self.city_D.id],
            'route_form_travel_time': 9,
        }
        form = RouteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_route_form(self):
        """ Тестирование формы поиска маршрута на не валидность"""

        data = {
            'from_city': self.city_A.id,
            'to_city': self.city_B.id,
            'cities': [self.city_E.id, self.city_D.id],
        }
        form = RouteForm(data=data)
        self.assertFalse(form.is_valid())

    def test_message_error_time(self):
        """ Тестирование сообщений об ошибках """

        data = {
            'from_city': self.city_A.id,
            'to_city': self.city_E.id,
            'cities': [self.city_C.id],
            'route_form_travel_time': 9,
        }
        response = self.client.post('/route_search/', data)
        self.assertContains(response, 'Время в дороге больше выбранного Вами. Измените время.', 1, HTTPStatus.OK)

    def test_message_error_through_cities(self):
        """ Тестирование сообщений об ошибках """

        data = {
            'from_city': self.city_B.id,
            'to_city': self.city_E.id,
            'cities': [self.city_C.id],
            'route_form_travel_time': 999,
        }
        response = self.client.post('/route_search/', data)
        self.assertContains(response, 'Нет маршрута через заданный город', 1, HTTPStatus.OK)
