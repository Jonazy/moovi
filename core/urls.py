from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('movies', views.MovieList.as_view(), name='movie_list'),
]