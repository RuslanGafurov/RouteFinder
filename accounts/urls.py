from django.urls import path

from accounts.views import *

urlpatterns = [
    path('login/', login_view, name='login'),
]
