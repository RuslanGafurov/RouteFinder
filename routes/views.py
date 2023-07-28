from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView

from routes.forms import RouteForm, RouteModelForm
from routes.models import Route
from routes.services import get_cleaned_form, get_routes, sort_trains

__all__ = (
    'add_route_view',
    'save_route_view',
    'RouteListView',
    'route_detail_view',
    'RouteDeleteView',
)


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
            form = get_cleaned_form(data)
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


def route_detail_view(request, pk=None):
    route = Route.objects.filter(pk=pk).first()
    trains = route.trains.all()
    sorted_trains = sort_trains(route, trains)
    context = {
        'route': route,
        'trains': sorted_trains,
    }
    return render(request, 'routes/detail.html', context)


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('routes:list')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Маршрут успешно удален')
        return self.delete(request, *args, **kwargs)
