from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from models import Thing, Opinion, Versus, VersusOpinion
from django.db.models import Q
from django.core import serializers
import json

def home(request):
    """Home view with a little introduction and maybe some aggregate data."""
    recent_opinions = Opinion.objects.all()[:10]
    random_things = Thing.get_random()
    return render_to_response('opinions/home.html', {'recent_opinions':
        recent_opinions, 'random_things': random_things},
        context_instance=RequestContext(request))

def index(request):
    """Show all the things."""
    things = Thing.objects.all()
    sort = request.GET.get('sort', 'name')
    if sort == 'rating':
        things = things.order_by('-rating')
    elif sort == 'unity':
        things = things.order_by('-unity')
    else:
        sort = 'name'

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
        return Http404()
    return render_to_response('opinions/versus.html', {'versus': v},
            context_instance=RequestContext(request))

def search(request, term=None):
    if not term and request.GET.get('term'):
        return redirect('search', request.GET.get('term'))
    elif not term:
        return redirect('home')
    """Oh boy."""
    things = Thing.objects.filter(name__icontains=term)

    return render_to_response('opinions/search.html', {'term': term, 'things':
        things}, context_instance=RequestContext(request))

def autocomplete(request, partial):
    things = Thing.objects.filter(name__istartswith=partial).order_by(
            'name')[:10]

    return HttpResponse(json.dumps(map(lambda thing: [thing.name,
            thing.get_absolute_url()], things)), mimetype="application/json")
