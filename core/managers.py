from django.db.models import Manager


class PersonManager(Manager):
    def all_with_prefect_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed',
            'writing_credits',
            'role_set_movie'
        )


class MovieManager(Manager):
    def all_with_prefect_persons(self):
        qs = self.get_queryset()
        qs.select_related(
            'director',
        )
        qs.prefetch_related(
            'writers',
            'actors',
        )
        return qs