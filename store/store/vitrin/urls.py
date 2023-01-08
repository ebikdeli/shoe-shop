from django.urls import path

from . import views


app_name = 'vitrin'

urlpatterns = [
    path('', views.users_view),
]
