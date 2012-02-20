from django.db import models
from django.contrib.auth.models import User

class Thing(models.Model):
    """A Thing we have Opinions about."""
    parent = models.ForeignKey('Thing', blank=True, null=True)
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.CharField(max_length=256, blank=True)

    class Meta(object):
        ordering = ['name']

class Opinion(models.Model):
    """An opinion of a Thing."""
    thing = models.ForeignKey('Thing')
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField()
    summary = models.CharField(max_length=256, blank=True)
    review = models.TextField()

    class Meta(object):
        ordering = ['-date']
        unique_together = ('user', 'thing')
