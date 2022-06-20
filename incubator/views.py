
from django.http import HttpResponseRedirect
from django.shortcuts import render
from actstream.models import Action
from django.contrib import messages
from django.urls import reverse

from space.fakeredis import get_redis, space_is_open
from realtime.helpers import feed_reducer

from constance import config as dyn_config

from wiki.models import Article


def error_view(code, msg):
    def view(request, exception=""):
        response = render(request, "error.html", {'code': code, 'message': msg})
        response.status_code = code
        return response
    return view


def home(request):
    client = get_redis()
    stream = []
    if request.user.is_authenticated:
        STREAM_SIZE = 20  # NOQA
        stream = Action.objects.filter(public=True).prefetch_related('target', 'actor', 'action_object')[:STREAM_SIZE * 2]
        stream = feed_reducer(stream)[:STREAM_SIZE]

    return render(request, "home.html", {
        "space_open": space_is_open(client),
        "message": dyn_config.HOMEPAGE_MESSAGE,
        "message_type": dyn_config.HOMEPAGE_MESSAGE_TYPE,
        "articles": Article.objects.all().filter(is_feeding_home_page=True),
        "stream": stream,
    })


def password_reset_done(request):
    messages.success(
        request,
        "Votre mot de passe a bien été réinitialisé, vous pouvez vous connecter avec votre nouveau mot de passe"
    )
    return HttpResponseRedirect(reverse('home'))


