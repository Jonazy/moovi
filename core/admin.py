from django.contrib import admin
from .models import Movie, Person, Vote, MovieImage, Role

# Register your models here.
admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Vote)
admin.site.register(MovieImage)
admin.site.register(Role)