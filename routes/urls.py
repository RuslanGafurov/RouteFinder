from django.urls import path

from routes.views import *

urlpatterns = [
    path('add_route/', add_route_view, name='add_route'),
    path('save_route/', save_route_view, name='save_route'),
    path('list/', RouteListView.as_view(), name='list'),
    path('detail/<int:pk>', RouteDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', RouteDeleteView.as_view(), name='delete'),
]
