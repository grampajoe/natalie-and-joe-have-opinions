from django.shortcuts import render_to_response
from django.templates import RequestContext
from django.contrib.auth.models import User
from models import Thing, Opinion

def home(request):
    """Home view with a little introduction and maybe some aggregate data."""
    recent_reviews = Review.objects.all()[10:]
    return render_to_response('opinions/home.html', {'recent_reviews':
            recent_reviews},
            context_instance=RequestContext(request))

def thing(request, thing_slug=None):
    """View a thing and the things they encompass."""
    if thing_slug is not None:
        thing = Thing.objects.get(slug=thing_slug)
        things = thing.thing_set.all()
    else:
        # We're at the top level
        thing = None
        things = Thing.objects.filter(parent__slug=thing_slug)
    return render_to_response('opinions/index.html', {'thing': thing,
            'things': things},
            context_instance=RequestContext(request))
