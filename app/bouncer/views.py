from google.cloud import ndb
from django.shortcuts import (
    redirect,
    render
)
from django.http import Http404
from bouncer.models import Redirect
# Create your views here.


def landing(request):
    redirects = Redirect.query().fetch()
    return render(request, 'bouncer/index.html', {'redirects': redirects})


def handle_redirect(request, slug):
    redirect_entity = ndb.Key(Redirect, slug).get()
    if not redirect_entity:
        raise Http404('not found')

    return redirect(redirect_entity.destination_url, permanent=True)