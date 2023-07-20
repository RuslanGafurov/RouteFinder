from django.urls import path

from cities.views import *

urlpatterns = [
    path('', cities_list_view, name='list'),
    path('detail/<int:pk>/', CityDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete'),
]
