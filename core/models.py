from django.db import models
from core.managers import (
    PersonManager,
    MovieManager,
    # VoteManager,
                           )
from users.models import CustomUser
from uuid import uuid4
from django.conf import settings

# Create your models here.


class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3

    RATINGS = (
        (NOT_RATED, 'NR - Not Rated'),
        (RATED_G, 'G - General Audience'),
        (RATED_PG, 'PR - Parental Guidance Suggested'),
        (RATED_R, 'R - Restricted'),
    )

    title = models.CharField(max_length=150)
    plot = models.TextField()
    year = models.PositiveBigIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    run_time = models.PositiveBigIntegerField()
    website = models.URLField(blank=True)
    director = models.ForeignKey(to='Person', on_delete=models.SET_NULL, related_name='directed',
                                 null=True, blank=True)
    writer = models.ManyToManyField(to='Person', related_name='writing_credits', blank=True)
    actor = models.ManyToManyField(to='Person', through='Role', related_name='acting_credits', blank=True)

    objects = MovieManager()

    class Meta:
        ordering = ('-year', 'title')

    def __str__(self):
        return self.title


class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)

    objects = PersonManager()

    class Meta:
        ordering = ('first_name', 'last_name')

    def __str__(self):
        if self.died:
            return '{}, {}, ({} - {})'.format(self.first_name, self.last_name, self.born, self.died)

        return '{}, {}, ({})'.format(self.first_name, self.last_name, self.born)


class Role(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(to=Person, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)

    def __str__(self):
        return '{}, {}, {}'.format(self.movie, self.person, self.name)

    class Meta:
        unique_together = ('movie', 'person', 'name')


class VoteManager(models.Manager):
    def get_vote_or_unsaved_blank_true(self, movie, user):
        try:
            return Vote.objects.get(
                movie=movie,
                user=user
            )
        except Vote.DoesNotExist:
            return Vote(
                movie=movie,
                user=user
            )


class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        ('UP', 'UP'),
        ('UP', 'DOWN'),
    )
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(to=CustomUser, related_name='user', on_delete=models.CASCADE)
    movie = models.ForeignKey(to=Movie, related_name='movie', on_delete=models.CASCADE)
    voted_on = models.DateField(auto_now=True)

    objects = VoteManager()

    class Meta:
        unique_together = ('user', 'movie')


def movie_directory_path_with_uuid(instance, filename):
    return '{}/{}'.format(
        instance.movie_id, uuid4()
    )


class MovieImage(models.Model):
    image = models.ImageField(upload_to=movie_directory_path_with_uuid)
    uploaded = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
