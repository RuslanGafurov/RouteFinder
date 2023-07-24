from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView

from cities.models import City
from routes.forms import RouteForm, RouteModelForm
from routes.models import Route
from routes.services import get_routes
from trains.models import Train


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


def add_route_view(request):
    if request.method == 'POST':
        context = {}
        data = request.POST
        if data:
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            total_time = int(data['total_time'])
            tmp_trains = data['trains'].split(',')
            trains_ids = [int(_id) for _id in tmp_trains if _id.isdigit()]
            trains = Train.objects.filter(id__in=trains_ids).select_related('from_city', 'to_city')
            cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()
            form = RouteModelForm(initial={
                'from_city': cities[from_city_id],
                'to_city': cities[to_city_id],
                'route_travel_time': total_time,
                'trains': trains,
            })
            context['form'] = form
        return render(request, 'routes/create.html', context)
    else:
        messages.error(request, 'Невозможно сохранить несуществующий маршрут')
        return redirect('/')


def save_route_view(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Маршрут успешно сохранен')
            return redirect('/')
        else:
            return render(request, 'routes/create.html', {'form': form})
    else:
        messages.error(request, 'Невозможно сохранить несуществующий маршрут')
        return redirect('/')


class RouteListView(ListView):
    model = Route
    template_name = 'routes/list.html'
    paginate_by = 3
