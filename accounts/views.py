from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from accounts.models import UserModel


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    success_message = 'Вы успешно вошли в аккаунт'


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = UserModel
    form_class = UserRegistrationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('accounts:login')
    success_message = 'Регистрация прошла успешно! Теперь Вы можете войти'


class UserProfileView(SuccessMessageMixin, UpdateView):
    model = UserModel
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_message = 'Данные успешно изменены'

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.object.pk})
