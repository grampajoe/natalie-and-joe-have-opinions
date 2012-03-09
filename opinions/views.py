from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import Http404
from models import Thing, Opinion, Tag, Versus, VersusOpinion
from django.db.models import Q

def home(request):
    """Home view with a little introduction and maybe some aggregate data."""
    recent_opinions = Opinion.objects.all()[:10]
    random_things = Thing.get_random()
    return render_to_response('opinions/home.html', {'recent_opinions':
        recent_opinions, 'random_things': random_things},
        context_instance=RequestContext(request))

def thing_index(request):
    """Show top-level things."""
    things = Thing.objects.filter(parent=None)
    return render_to_response('opinions/index.html', {'things': things},
            context_instance=RequestContext(request))

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

def tag(request, name):
    tag = get_object_or_404(Tag, name=name)
    return render_to_response('opinions/tag.html', {'tag': tag},
            context_instance=RequestContext(request))

def search(request, term):
    """Oh boy."""
    things = Thing.objects.filter(Q(tags__name__icontains=term) |
            Q(name__icontains=term))
    tags = Tag.objects.filter(name__icontains=term)

    results = {'things': things, 'tags': tags}

    return render_to_response('opinions/search.html', {'term': term, 'results':
        results}, context_instance=RequestContext(request))
