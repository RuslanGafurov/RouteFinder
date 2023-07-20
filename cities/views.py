from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView, ListView

from cities.forms import CityForm
from cities.models import City

__all__ = (
    'CityListView',
    'CityDetailView',
    'CityUpdateView',
    'CityDeleteView',
)


class CityListView(ListView):
    model = City
    template_name = 'cities/list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data(**kwargs)
        context['form'] = CityForm()
        return context


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityUpdateView(UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:list')


class CityDeleteView(DeleteView):
    model = City
    success_url = reverse_lazy('cities:list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
