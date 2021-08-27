from django.db.models import Manager
from django.db.models.aggregates import Sum


class PersonManager(Manager):
    def all_with_prefect_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed',
            'writing_credits',
            'acting_credits'
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

    def all_with_related_persons_and_score(self):
        qs = self.all_with_prefect_persons()
        qs = qs.annotate(score=Sum('movie__value'))
        return qs

    def top_movies(self, limit=10):
        qs = self.get_queryset()
        qs = qs.annotate(
            vote_sum=Sum('movie__value'))
        qs = qs.exclude(vote_sum=None)
        qs = qs.order_by('-vote_sum')
        qs = qs[:limit]
        return qs



# class VoteManager(Manager):
#     def get_vote_or_unsaved_blank_true(self, movie, user):
#         try:
#             return self.Vote.objects.get(
#                 movie=movie,
#                 user=user
#             )
#         except self.Vote.DoesNotExist:
#             return self.Vote(
#                 movie=movie,
#                 user=user
#             )