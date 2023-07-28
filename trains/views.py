from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from trains.forms import TrainForm
from trains.models import Train

__all__ = (
    'TrainListView',
    'TrainCreateView',
    'TrainDetailView',
    'TrainUpdateView',
    'TrainDeleteView',
)


class TrainListView(ListView):
    model = Train
    template_name = 'trains/list.html'
    paginate_by = 5


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('trains:list')
    success_message = 'Поезд успешно добавлен'


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('trains:list')
    success_message = 'Поезд успешно изменен'


class TrainDeleteView(LoginRequiredMixin, DeleteView):
    model = Train
    success_url = reverse_lazy('trains:list')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Поезд успешно удален')
        return self.delete(request, *args, **kwargs)
