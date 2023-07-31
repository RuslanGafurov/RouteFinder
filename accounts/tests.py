from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.models import UserModel
from common.tests import common_tests


class UserRegistrationTest(TestCase):

    def setUp(self) -> None:
        self.path = reverse('accounts:registration')
        self.data = {
            'username': 'Test',
            'password1': 'asFFcv68g',
            'password2': 'asFFcv68g',
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        common_tests(self, response, 'accounts/registration.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(UserModel.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('accounts:login'))
        self.assertTrue(UserModel.objects.filter(username=username).exists())

    def test_user_registration_post_error(self):
        UserModel.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserLoginTest(TestCase):

    def test_user_login(self):
        path = reverse('accounts:login')
        response = self.client.get(path)

        common_tests(self, response, 'accounts/login.html')
