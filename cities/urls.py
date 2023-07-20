from django.urls import path

from cities.views import *

urlpatterns = [
    path('list', cities_list_view, name='list')
]
