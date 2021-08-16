from django.shortcuts import render
from core.models import Movie
from django.views.generic import ListView, DetailView


# Create your views here.


class MovieList(ListView):
    model = Movie
    # template_name = 'core/movie_list.html'
