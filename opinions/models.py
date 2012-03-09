from django.db import models
from django.contrib.auth.models import User
import random

class Thing(models.Model):
    """A Thing we have Opinions about."""
    parent = models.ForeignKey('Thing', blank=True, null=True,
            related_name='children')
    name = models.CharField(max_length=256)
    slug = models.SlugField(db_index=True, unique=True)
    description = models.CharField(max_length=256, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    versus = models.ManyToManyField('Thing', through='Versus',
            symmetrical=False)

    def get_opinions(self):
        opinions = []
        for name in ('Natalie', 'Joe'):
            try:
                opinions.append(self.opinions.get(user__first_name=name))
            except Opinion.DoesNotExist:
                opinions.append(False)
        return opinions

    def get_versus(self, count=None):
        """Get all Versus objects related to this one."""
        return Versus.objects.filter(models.Q(thing_one=self) |
                models.Q(thing_two=self))[:count]

    @staticmethod
    def get_random():
        n = 10
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

class Review(models.Model):
    """Abstract class for objects containing reviews, Opinions and Versuses."""
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)
    summary = models.CharField(max_length=256, blank=True)
    review = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True)

    class Meta(object):
        abstract = True
        ordering = ['-date']

class Opinion(Review):
    """An opinion of a Thing."""
    thing = models.ForeignKey('Thing', related_name='opinions')
    rating = models.FloatField()
    
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

class Versus(models.Model):
    thing_one = models.ForeignKey('Thing', related_name='versus_one')
    thing_two = models.ForeignKey('Thing', related_name='versus_two')
    description = models.CharField(max_length=256, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    @staticmethod
    def get_by_slugs(slug1, slug2):
        return Versus.objects.get(models.Q(thing_one__slug=slug1,
                thing_two__slug=slug2) | models.Q(thing_one__slug=slug2,
                thing_two__slug=slug1))

    def get_things(self):
        """Get a consistently ordered list of things."""
        return sorted([self.thing_one, self.thing_two], key=lambda thing: thing.name);

    def get_opinions(self):
        opinions = []
        for name in ('Natalie', 'Joe'):
            try:
                opinion = self.opinions.get(user__first_name=name)
            except VersusOpinion.DoesNotExist:
                opinion = False
            opinions.append(opinion)
        return opinions

    def __unicode__(self):
        return '{0} vs. {1}'.format(*self.get_things())

    @models.permalink
    def get_absolute_url(self):
        # Randomly order slugs so the URL doesn't give it away.
        return ('versus', map(lambda thing: thing.slug, self.get_things()))

    class Meta(object):
        unique_together = ('thing_one', 'thing_two')

class VersusOpinion(Review):
    versus = models.ForeignKey('Versus', related_name='opinions')
    winner = models.ForeignKey('Thing', related_name='versus_wins', blank=True,
            null=True)

    class Meta(object):
        unique_together = ('user', 'versus')

class Tag(models.Model):
    name = models.SlugField(max_length=64, primary_key=True)

    def __unicode__(self):
        return u'#{0}'.format(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('tag', [self.name])

    class Meta(object):
        ordering = ['name']
