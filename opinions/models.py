from django.db import models
from django.contrib.auth.models import User
import random

class Thing(models.Model):
    """A Thing we have Opinions about."""
    parent = models.ForeignKey('Thing', blank=True, null=True)
    name = models.CharField(max_length=256)
    slug = models.SlugField(db_index=True, unique=True)
    description = models.CharField(max_length=256, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def get_opinions(self):
        opinions = []
        for name in ('Natalie', 'Joe'):
            try:
                opinions.append(self.opinion_set.get(user__first_name=name))
            except:
                opinions.append(None)
        return opinions

    @staticmethod
    def get_random():
        n = 2
        count = Thing.objects.all().count()
        if (count >= n):
            things = set([])
            max_id = Thing.objects.aggregate(models.Max('id'))['id__max']
            while len(things) < n:
                ids = random.sample(xrange(1, max_id+1), n)
                things.update(Thing.objects.filter(id__in=ids))
            return list(things)
        else:
            return Thing.objects.order_by('?')

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('thing', [self.slug])

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
    
    def __unicode__(self):
        if len(self.summary):
            return u'{0} on {1}: "{2}"'.format(self.user.first_name,
                    self.thing.name, self.summary)
        else:
            return u'{0} on {1}'.format(self.user.first_name, self.thing.name)

    def get_absolute_url(self):
        return self.thing.get_absolute_url()

    class Meta(object):
        ordering = ['-date']
        unique_together = ('user', 'thing')

class Tag(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    def __unicode__(self):
        return self.name

    class Meta(object):
        pass
