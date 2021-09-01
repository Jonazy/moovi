import django
from django.shortcuts import render, redirect
from django.urls import reverse
from core.models import Movie, Vote, Person
from core.forms import VoteForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from core.mixins import CachPageVaryOnCookieMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.core.cache import cache


# Create your views here.


class MovieList(CachPageVaryOnCookieMixin, ListView):
    model = Movie
    context_object_name = 'movies'
    paginate_by = 10
    template_name = 'core/movie_list.html'


class MovieDetail(LoginRequiredMixin, DetailView):
    template_name = 'core/detail.html'
    queryset = (
        Movie.objects
            .all_with_related_persons_and_score())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_true(
                movie=self.object,
                user=self.request.user,
            )
            if vote.id:
                vote_form_url = reverse(
                    'core:vote_update',
                    kwargs={
                        'movie_id': vote.movie.id,
                        'pk': vote.id
                    }
                )
            else:
                vote_form_url = reverse(
                    'core:vote',
                    kwargs={
                        'movie_id': self.object.id
                    })
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
        return ctx


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm
    template_name = 'core/detail.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse(
            'core:movie_detail',
            kwargs={'pk': movie_id}
        )

    # def render_to_response(self, context, **response_kwargs):
    #     movie_id = context['object'].id
    #     movie_detail_url = reverse(
    #         'core:movie_detail',
    #         kwargs={'pk': movie_id}
    #     )
    #     return redirect(to=movie_detail_url)


class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm

    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied('Cannot change another user vote')
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        movie_detail_url = reverse(
            'core:movie_detail',
            kwargs={
                'pk': movie_id
            }
        )
        return movie_detail_url


class TopMovies(LoginRequiredMixin, ListView):
    template_name = 'core/top_movie_list.html'
    context_object_name = 'top_movies'
    queryset = Movie.objects.top_movies
    # def get_queryset(self):
    #     limit = 10
    #     key = 'top_movies_%s' % limit
    #     cached_qs = cache.get(key)
    #     if cached_qs:
    #         same_django = cached_qs._django_version == django.get_version()
    #         if same_django:
    #             return cached_qs
    #     qs = Movie.objects.top_movies(limit=limit)
    #     cache.set(key, qs)
    #     return qs
    # queryset = Movie.objects.top_movies(
    #     limit=10
    # )


class PersonDetail(LoginRequiredMixin, DetailView):
    queryset = Person.objects.all_with_prefect_movies()
    template_name = 'core/person_detail.html'


class AboutPage(TemplateView):
    template_name = 'core/about.html'


class FAQsPage(TemplateView):
    template_name = 'core/FAQs.html'