from django.shortcuts import render
from django.views.generic import DetailView

from cities.models import City

__all__ = (
    'cities_list_view',
    'CityDetailView',
)


def cities_list_view(request):
    query_set = City.objects.all()
    context = {'objects_list': query_set}
    return render(request, 'cities/list.html', context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'
