from django.contrib import admin

from routes.models import Route


class RouteAdmin(admin.ModelAdmin):
    class Meta:
        model = Route

    list_display = ('name', 'from_city', 'to_city', 'route_travel_time')
    list_editable = ('route_travel_time',)


admin.site.register(Route, RouteAdmin)
