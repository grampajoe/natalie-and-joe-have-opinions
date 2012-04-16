from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
from django.core.files import File
import tempfile
import random
import markdown
import os
import re

class HasPictures(object):
    def insert_pictures(self, mdstr):
        """Replace picture pseudo-markdown with actual markdown."""
        pictures = self.pictures.all()
        for picture in pictures:
            if not picture.label or not len(picture.label):
                continue

            if picture.description and len(picture.description):
                fmt = u'<a class="image" href="{2}">'+\
                        '![{0}]({1})<span>{0}</span></a>'
            else:
                fmt = u'<a class="image" href="{2}">![{0}]({1})</a>'
            mdstr = re.sub(r'\?\[{0}\]'.format(picture.label),
                    fmt.format(picture.description,
                        picture.thumbnail.url, picture.image.url), mdstr)
        return mdstr

class Thing(HasPictures, models.Model):
    """A Thing we have Opinions about."""
    parent = models.ForeignKey('Thing', blank=True, null=True,
            related_name='children')
    name = models.CharField(max_length=255, db_index=True, unique=True)
    image = models.ImageField(upload_to="images/things/", blank=True)
    slug = models.SlugField(db_index=True)
    versus = models.ManyToManyField('Thing', through='Versus',
            symmetrical=False)
    rating = models.FloatField(blank=True, null=True, db_index=True)
    unity = models.FloatField(blank=True, null=True, db_index=True)

    def get_opinions(self):
        opinions = []
        for name in ('Natalie', 'Joe'):
            try:
                opinions.append(self.opinions.get(user__first_name=name))
            except Opinion.DoesNotExist:
                opinions.append(False)
        return opinions

    def update_ratings(self):
        opinions = self.opinions.all()

        # Rating is the average of all ratings
        rating = reduce(lambda a, b: a + b.rating, opinions, 0)
        rating /= len(opinions) or 1
        self.rating = rating
        
        # Unity is the maximum rating minus the absolute difference between ratings
        if len(opinions) > 1:
            self.unity = settings.MAX_RATING - reduce(lambda a, b: abs(a.rating -
                    b.rating), opinions)
        else:
            # Unity is undefined if one hasn't rated
            self.unity = None
        self.save()

    def get_versus(self, count=None):
        """Get all Versus objects related to this one."""
        return Versus.objects.filter(models.Q(thing_one=self) |
                models.Q(thing_two=self))[:count]

    def get_parents(self):
        p = self.parent
        ps = []
        if p is not None:
            ps.append(p)
            ps.extend(p.get_parents())
        return ps

    @staticmethod
    def get_random():
        n = 10
        count = Thing.objects.all().count()
        if (count > n):
            things = set([])
            max_id = Thing.objects.aggregate(models.Max('id'))['id__max']
            while len(things) < n:
                ids = random.sample(xrange(1, max_id+1), n)
                things.update(Thing.objects.filter(id__in=ids))
            things = list(things)
            random.shuffle(things)
            return things
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
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    summary = models.CharField(max_length=256, blank=True)
    review = models.TextField()

    def html_review(self):
        return markdown.markdown(self.get_review())

    class Meta(object):
        abstract = True
        ordering = ['-date']

class Opinion(Review):
    """An opinion of a Thing."""
    thing = models.ForeignKey('Thing', related_name='opinions')
    rating = models.FloatField()

    def get_review(self):
        return self.thing.insert_pictures(self.review)
    
    def inverse_rating(self):
        return settings.MAX_RATING - self.rating

    def __unicode__(self):
        return unicode(self.thing)

    def get_absolute_url(self):
        return self.thing.get_absolute_url()

    def save(self, *args, **kwargs):
        super(Opinion, self).save(*args, **kwargs)
        self.thing.update_ratings()

    def delete(self, *args, **kwargs):
        thing = self.thing
        super(Opinion, self).delete(*args, **kwargs)
        thing.update_ratings()

    class Meta(object):
        ordering = ['-date']
        unique_together = ('user', 'thing')

class Picture(models.Model):
    thing = models.ForeignKey('Thing', related_name='pictures', blank=True,
            null=True)
    versus = models.ForeignKey('Versus', related_name='pictures', blank=True,
            null=True)
    image = models.ImageField(upload_to='images/things/')
    thumbnail = models.ImageField(upload_to='images/things/thumbs/',
            blank=True)
    description = models.CharField(max_length=255, blank=True)
    label = models.CharField(max_length=32, blank=True)

    thumb_size = (365,400)

    def save(self, *args, **kwargs):
        """Generate a thumbnail."""
        super(Picture, self).save(*args, **kwargs)
        image = Image.open(self.image.path)
        thumb = image.copy()
        thumb.thumbnail(self.thumb_size, Image.ANTIALIAS)
        fp, tmppath = tempfile.mkstemp()
        thumb.save(tmppath, image.format)
        self.thumbnail.save(self.image.name, File(open(tmppath)), save=False)
        os.unlink(tmppath)
        super(Picture, self).save(*args, **kwargs)

class Versus(HasPictures, models.Model):
    thing_one = models.ForeignKey('Thing', related_name='versus_one')
    thing_two = models.ForeignKey('Thing', related_name='versus_two')

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
        return u'{0} vs {1}'.format(unicode(self.thing_one),
                unicode(self.thing_two))

    @models.permalink
    def get_absolute_url(self):
        """URLs are alphabetical, too."""
        return ('versus', map(lambda thing: thing.slug, self.get_things()))

    def save(self, *args, **kwargs):
        """Save in alphabetical order."""
        if self.thing_one.name > self.thing_two.name:
            temp = self.thing_one
            self.thing_one = self.thing_two
            self.thing_two = temp
        super(Versus, self).save(*args, **kwargs)

    class Meta(object):
        unique_together = ('thing_one', 'thing_two')
        verbose_name_plural = 'versuses'

class VersusOpinion(Review):
    versus = models.ForeignKey('Versus', related_name='opinions')
    winner = models.ForeignKey('Thing', related_name='versus_wins', blank=True,
            null=True)

    def get_review(self):
        return self.versus.insert_pictures(self.review)

    def __unicode__(self):
        return unicode(self.versus)

    def get_absolute_url(self):
        return self.versus.get_absolute_url()

    class Meta(object):
        unique_together = ('user', 'versus')
