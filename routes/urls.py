from django.urls import path

from routes.views import add_route_view

urlpatterns = [
    path('add_route/', add_route_view, name='add_route'),
]
