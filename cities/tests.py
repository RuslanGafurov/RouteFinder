from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from cities.models import City
from cities.views import CityListView


class CitiesAllTests(TestCase):
    fixtures = ['cities.json']

    def setUp(self) -> None:
        self.cities = City.objects.all()

    def _common_tests(self, response, view):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        if view == 'list':
            self.assertTemplateUsed(response, template_name='cities/list.html')
        elif view == 'detail':
            self.assertTemplateUsed(response, template_name='cities/detail.html')

        # self.assertEqual(response.context_data['title'], 'Title')

    def test_city_list_view(self):
        path = reverse('cities:list')
        response = self.client.get(path)
        index = CityListView.paginate_by

        self._common_tests(response, 'list')
        self.assertEqual(list(response.context_data['object_list']), list(self.cities)[:index])

    def test_city_detail_view(self):
        path = reverse('cities:detail', kwargs={'pk': self.cities[0].id})
        response = self.client.get(path)

        self._common_tests(response, 'detail')
