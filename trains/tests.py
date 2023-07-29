from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from trains.models import Train
from trains.views import TrainListView


class TrainsAllTests(TestCase):
    fixtures = ['cities.json', 'trains.json']

    def setUp(self) -> None:
        self.trains = Train.objects.all()

    def _common_tests(self, response, view):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        if view == 'list':
            self.assertTemplateUsed(response, template_name='trains/list.html')
        elif view == 'detail':
            self.assertTemplateUsed(response, template_name='trains/detail.html')

        # self.assertEqual(response.context_data['title'], 'Title')

    def test_train_list_view(self):
        path = reverse('trains:list')
        response = self.client.get(path)
        index = TrainListView.paginate_by

        self._common_tests(response, 'list')
        self.assertEqual(list(response.context_data['object_list']), list(self.trains)[:index])

    def test_train_detail_view(self):
        path = reverse('trains:detail', kwargs={'pk': self.trains[0].id})
        response = self.client.get(path)

        self._common_tests(response, 'detail')
