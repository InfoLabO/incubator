from datetime import timedelta
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.edit import DeleteView
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.db import IntegrityError
from django.core.paginator import Paginator

from influxdb import InfluxDBClient
from rest_framework import viewsets
from rest_framework.response import Response

from .djredis import get_redis, set_space_open, space_is_open
from .forms import MacAdressForm
from .models import SpaceStatus, MacAdress
from .serializers import PamelaSerializer, SpaceStatusSerializer
from .decorators import private_api, one_or_zero
from .helpers import is_stealth_mode, make_empty_pamela, make_pamela, user_should_see_pamela
from users.models import User
from realtime.helpers import publish_space_state

from django.conf import settings


def pamela_list(request):
    if request.method == 'POST':
        form = MacAdressForm(request.POST)
        if form.is_valid():
            mac = form.save(commit=False)
            mac.holder = request.user
            mac.save()
            messages.success(request, 'Votre MAC a été ajoutée !')

            return HttpResponseRedirect(reverse('pamela_list'))
    else:
        form = MacAdressForm()

    context = make_pamela()
    del context['hidden_users']
    context['form'] = form
    context['space_open'] = space_is_open(get_redis())
    context['status_change'] = SpaceStatus.objects.last()

    context["stealth_mode"] = is_stealth_mode()
    context["should_show_pamela"] = user_should_see_pamela(request.user)

    return render(request, "pamela.html", context)


@private_api()
def get_user_mac(request):
    qs = User.objects.all()
    users = {x.username: [m.adress for m in x.macadress_set.all()] for x in qs}
    return JsonResponse(users, safe=False)


@private_api()
def get_mac_user(request):
    qs = MacAdress.objects.exclude(holder=None).select_related("holder")
    macs = {x.adress: x.holder.username for x in qs}
    return JsonResponse(macs, safe=False)


@private_api()
def full_pamela(request):
    data = make_pamela()
    pool = list(data['unknown_mac']) + [u.username for u in (data['hidden_users'] | data['users'])]
    return JsonResponse(pool, safe=False)


@private_api(open=one_or_zero)
def status_change(request, open):
    r = {'open': open}
    if bool(open) != space_is_open(get_redis()):
        set_space_open(get_redis(), open)
        publish_space_state(open)
    return JsonResponse(r, safe=False)


class DeleteMACView(DeleteView):
    model = MacAdress
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        obj = super(DeleteMACView, self).get_object()
        if not obj.holder == self.request.user:
            raise PermissionDenied
        return obj


def get_sensors(*sensors):
    query_template = "SELECT value FROM %s ORDER BY time DESC LIMIT 1"
    queries = ';'.join(query_template % s for s in sensors)
    influx_credentials = (settings.INFLUX_HOST, settings.INFLUX_PORT, settings.INFLUX_USER, settings.INFLUX_PASS)
    client = InfluxDBClient(*influx_credentials, timeout=1)
    r = client.query(queries, database="hal")
    if len(sensors) == 1:
        return {sensors[0]: next(r.get_points())['value']}
    else:
        return {k: next(v.get_points())['value'] for k, v in zip(sensors, r)}


@cache_page(30)
def spaceapi(request):
    client = get_redis()
    if is_stealth_mode():
        pam = make_empty_pamela()
    else:
        pam = make_pamela()

    users = [u.username for u in pam['users']]
    names = pam['unknown_mac'] + users

    if len(names) == 0:
        people_now_present = {
            "value": pam['hidden'],
        }
    else:
        people_now_present = {
            "value": len(names) + pam['hidden'],
            "names": names,
        }

    keymasters = [
        {
            'name': user.username,
            # 'irc_nick':,
            # 'email':,
        }
        for user in User.objects.filter(has_key=True)
    ]

    response = {
        "api": "0.13",
        "space": "InfoLabO",
        "logo": "https://infolabo/static/img/space-invaders.png",
        "url": "https://infolabo.org",
        "location": {
            "lat": 50.812915,
            "lon": 4.384396,
            "address": "6 Rue Léonard de Vinci, 45067 Orléans",
        },
        "state": {
            "open": space_is_open(client),
            "lastchange": round(SpaceStatus.objects.last().time.timestamp()),
            "icon": {
                "open": "https://infolab.org/static/img/space-invaders-open.png",
                "closed": "https://infolabo.org/static/img/space-invaders.png"
            }
        },
        # "events": {},
        "contact": {
            "issue_mail": "contact@infolabo.org",
            "email": "contact@infolabo.org",
            "phone": "+33",
            "keymasters": keymasters,
        },
        "issue_report_channels": [
            "issue_mail",
            "twitter"
        ],
        "sensors": {
            "people_now_present": [people_now_present],
            # "beverage_supply": [42],
            # "temperature": [],
        },
        # "feeds": {
        #     "calendar": "",
        # },
        "projects": [
            "https://infolabo.org/projects/",
            "https://github.com/InfoLabo",
        ],
    }

    try:
        sensors = get_sensors('light_inside', 'light_outside', 'door_stairs')
        response["sensors"]["door_locked"] = [{
            "value": sensors['door_stairs'] == 0,
            "location": "stairs",
            "name": "door_stairs"
        }]
        response["sensors"]["light"] = [{
            "value": round(100 * sensors['light_%s' % loc], 2),
            "unit": '%',
            "location": loc,
            "name": 'light_%s' % loc
        } for loc in ('inside', 'outside')]
    except Exception:
        pass

    return JsonResponse(response)


def openings_data(request):
    # opts = {k: request.GET[k] for k in request.GET}
    return JsonResponse({
        'probs': 0,  # list(weekday_probs(opts)),
        'range': 0,  # human_time(opts),
    })


class PamelaObject(object):
    def __init__(self, pamela_dict):
        last_updated = timezone.now() - timedelta(seconds=pamela_dict['updated'])

        self.total_mac_count = len(pamela_dict['raw_maclist'])
        self.last_updated = last_updated
        self.age = pamela_dict['updated']
        self.unknown_mac = pamela_dict['unknown_mac']
        self.users = pamela_dict['users']
        self.hidden = pamela_dict['hidden']


class PamelaViewSet(viewsets.ViewSet):
    def list(self, request):
        if user_should_see_pamela(request.user):
            pam_dict = make_pamela()
        else:
            pam_dict = make_empty_pamela()

        pam = PamelaObject(pam_dict)
        serializer = PamelaSerializer(pam)
        return Response(serializer.data)


class OpeningsViewSet(viewsets.ModelViewSet):
    queryset = SpaceStatus.objects.all().order_by('-time')
    serializer_class = SpaceStatusSerializer


