from django.test import TestCase
from django.urls import reverse

from common.tests import common_tests
from trains.models import Train
from trains.views import TrainListView


class TrainsAllTests(TestCase):
    fixtures = ['cities.json', 'trains.json']

    def setUp(self) -> None:
        self.trains = Train.objects.all()

    def test_train_list_view(self):
        path = reverse('trains:list')
        response = self.client.get(path)
        index = TrainListView.paginate_by

        common_tests(self, response, 'trains/list.html')
        self.assertEqual(list(response.context_data['object_list']), list(self.trains)[:index])

    def test_train_detail_view(self):
        path = reverse('trains:detail', kwargs={'pk': self.trains[0].id})
        response = self.client.get(path)

        common_tests(self, response, 'trains/detail.html')
