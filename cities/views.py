from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView

from cities.forms import CityForm
from cities.models import City

__all__ = (
    'cities_list_view',
    'CityDetailView',
    'CityDeleteView',
)


def cities_list_view(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    form = CityForm()
    query_set = City.objects.all()
    context = {
        'objects_list': query_set,
        'form': form,
    }
    return render(request, 'cities/list.html', context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityDeleteView(DeleteView):
    model = City
    success_url = reverse_lazy('cities:list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
