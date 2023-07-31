from django.test import TestCase
from django.urls import reverse

from cities.models import City
from cities.views import CityListView
from common.tests import common_tests


class CitiesAllTests(TestCase):
    fixtures = ['cities.json']

    def setUp(self) -> None:
        self.cities = City.objects.all()

    def test_city_list_view(self):
        path = reverse('cities:list')
        response = self.client.get(path)
        index = CityListView.paginate_by

        common_tests(self, response, 'cities/list.html')
        self.assertEqual(list(response.context_data['object_list']), list(self.cities)[:index])

    def test_city_detail_view(self):
        path = reverse('cities:detail', kwargs={'pk': self.cities[0].id})
        response = self.client.get(path)

        common_tests(self, response, 'cities/detail.html')
