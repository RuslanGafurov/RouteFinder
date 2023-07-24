from django.urls import path

from routes.views import add_route_view, save_route_view, RouteListView

urlpatterns = [
    path('add_route/', add_route_view, name='add_route'),
    path('save_route/', save_route_view, name='save_route'),
    path('list/', RouteListView.as_view(), name='list'),
]
