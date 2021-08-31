from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('movies/', views.MovieList.as_view(), name='movie_list'),
    path('movie/<int:pk>/', views.MovieDetail.as_view(), name='movie_detail'),
    path('movie/<int:movie_id>/vote/', views.CreateVote.as_view(), name='vote'),
    path('movie/<int:movie_id>/vote/<int:pk>/', views.UpdateVote.as_view(), name='vote_update'),
    path('movies/top/', views.TopMovies.as_view(), name='top_movies'),
    path('person/<int:pk>/', views.PersonDetail.as_view(), name='person_detail'),
    path('about/', views.AboutPage.as_view(), name='about_page'),
    path('FAQs/', views.FAQsPage.as_view(), name='FAQs_page'),
    path('topmovies/', views.TopMovies.as_view(), name='top_movies'),
]