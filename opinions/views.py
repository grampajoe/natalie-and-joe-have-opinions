from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from models import Thing, Opinion, Versus, VersusOpinion
from django.db.models import Q
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib.syndication.views import Feed
import json

def home(request):
    """Home view with a little introduction and maybe some aggregate data."""
    recent_opinions = Opinion.objects.all()[:10]
    recent_versus = VersusOpinion.objects.all()[:10]
    recent = sorted(list(recent_opinions) + list(recent_versus),
            key=lambda r: r.date, reverse=True)[:10]
    random_things = Thing.get_random()
    return render_to_response('opinions/home.html', {'recent_opinions':
        recent, 'random_things': random_things},
        context_instance=RequestContext(request))

def index(request):
    """Show all the things."""
    things = Thing.objects.all()
    sort = request.GET.get('sort', 'name')
    if sort == 'rating':
        things = things.order_by('-rating')
    elif sort == 'unity':
        things = things.order_by('-unity')
    #elif sort == 'date':
    #    things = things.order_by('-opinions__date').distinct()
    else:
        sort = 'name'

    paginator = Paginator(things, settings.THINGS_PER_PAGE)

    page = request.GET.get('page', 1)
    try:
        things = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        things = paginator.page(1)

    return render_to_response('opinions/index.html', {'things': things, 'sort':
            sort}, context_instance=RequestContext(request))

def thing(request, thing_slug):
    """View a thing and the things they encompass."""
    thing = get_object_or_404(Thing, slug=thing_slug)
    return render_to_response('opinions/thing.html', {'thing': thing},
            context_instance=RequestContext(request))

def versus(request, slug1, slug2):
    if slug1 > slug2:
        # Not in alphabetical order
        return redirect(versus, slug2, slug1, permanent=True)

    try:
        v = Versus.get_by_slugs(slug1, slug2)
    except Versus.DoesNotExist:
        raise Http404()
    return render_to_response('opinions/versus.html', {'versus': v},
            context_instance=RequestContext(request))

def search(request, term=None):
    if not term and request.GET.get('term'):
        return redirect('search', request.GET.get('term'))
    elif not term:
        return redirect('home')
    """Oh boy."""
    things = Thing.objects.filter(name__icontains=term)

    paginator = Paginator(things, settings.THINGS_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        things = paginator.page(page)
    except InvalidPage:
        things = paginator.page(1)

    return render_to_response('opinions/search.html', {'term': term, 'things':
        things}, context_instance=RequestContext(request))

def autocomplete(request, partial):
    things = Thing.objects.filter(name__istartswith=partial).order_by(
            'name')[:10]

    return HttpResponse(json.dumps(map(lambda thing: [thing.name,
            thing.get_absolute_url()], things)), mimetype="application/json")


class RecentOpinionsRSS(Feed):
    title = "Natalie and Joe Have Opinions About Literally Everything"
    link = "/"
    description = "Opinions from Natalie and Joe."

    def items(self):
        recent_opinions = Opinion.objects.all()[:10]
        recent_versus = VersusOpinion.objects.all()[:10]
        recent = sorted(list(recent_opinions) + list(recent_versus),
                key=lambda r: r.date, reverse=True)[:10]
        return recent

    def item_title(self, item):
        return u'{0} on {1}'.format(item.user.first_name, unicode(item))

    def item_description(self, item):
        return None

    def item_pubdate(self, item):
        return item.date
