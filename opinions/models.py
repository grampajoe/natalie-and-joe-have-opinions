from django.db import models
from django.contrib.auth.models import User

class Thing(models.Model):
    """A Thing we have Opinions about."""
    parent = models.ForeignKey('Thing', blank=True, null=True)
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.CharField(max_length=256, blank=True)

    def get_opinions(self):
        opinions = []
        for name in ('Natalie', 'Joe'):
            try:
                opinions.append(self.opinion_set.get(user__first_name=name))
            except:
                opinions.append(None)
        return opinions

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
        return u'{0} by {1}'.format(self.thing.name, self.user.username)

    def get_absolute_url(self):
        return self.thing.get_absolute_url()

    class Meta(object):
        ordering = ['-date']
        unique_together = ('user', 'thing')
