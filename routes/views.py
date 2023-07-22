from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView

from routes.forms import RouteForm
from routes.models import Route
from routes.services import get_routes


def route_search_view(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
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


class RouteListView(ListView):
    model = Route
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(RouteListView, self).get_context_data(**kwargs)
        context['form'] = RouteForm()
        return context
