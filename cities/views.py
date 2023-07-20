from django.shortcuts import render

from cities.models import City

__all__ = (
    'cities_list_view',
)


def cities_list_view(request):
    query_set = City.objects.all()
    context = {'objects_list': query_set}
    return render(request, 'cities/list.html', context)
