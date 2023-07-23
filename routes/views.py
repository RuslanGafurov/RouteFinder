from django.contrib import messages
from django.shortcuts import render

from routes.forms import RouteForm
from routes.services import get_routes


def home_view(request):
    form = RouteForm()
    return render(request, 'home.html', {'form': form})


def route_search_view(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(form)
            except ValueError as err:
                messages.error(request, err)
                return render(request, 'home.html', {'form': form})
            return render(request, 'home.html', context)
        else:
            return render(request, 'home.html', {'form': form})
    else:
        form = RouteForm()
        messages.error(request, 'Нет данных для поиска')
        return render(request, 'home.html', {'form': form})
