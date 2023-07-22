from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView, ListView, CreateView

from routes.forms import RouteForm
from routes.models import Route


class RouteListView(ListView):
    model = Route
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(RouteListView, self).get_context_data(**kwargs)
        context['form'] = RouteForm()
        return context
