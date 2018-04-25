"""

SCL <scott@rerobots.net>
2018
"""
from __future__ import absolute_import

import base64
from datetime import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
import jwt
import requests

from cryptography.x509 import load_der_x509_certificate
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from . import views
from . import tasks
from .models import SimJob
from .settings import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_REDIRECT_URI, AUTH0_TENANT_DOMAIN


def index(request):
    context = {
        'jobs': [],
    }
    try:
        for job in SimJob.objects.iterator():
            context['jobs'].append({
                'starttime': job.starttime.strftime('%a, %d %b %Y %T %z'),
                'result': job.result,
                'done': job.done,
            })
    except:
        pass
    return render(request, 'acarbroker/index.html', context)


def submit(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('signin'))
    MAX_FILESIZE = 5 * 2**20
    context = {
        'prescreen': None,
    }
    if 'user_upload' in request.FILES:
        context['prescreen'] = True
        if request.FILES['user_upload'].size > MAX_FILESIZE:
            context['prescreen'] = False
            context['prescreen_reason'] = 'The submitted file is too big.'
        chunks = []
        acc = 0
        for chunk in request.FILES['user_upload'].chunks():
            chunks.append(str(base64.b64encode(chunk), encoding='utf-8'))
            acc += len(chunk)
            if acc > MAX_FILESIZE:
                context['prescreen'] = False
                context['prescreen_reason'] = 'The submitted file is too big.'
        if context['prescreen']:
            job = SimJob.objects.create(user=request.user,
                                        starttime=datetime.utcnow())
            job.save()
            tasks.simjob.delay(chunks, job.pk)
    return render(request, 'acarbroker/submit.html', context)


def signin(request):
    if request.user.is_authenticated:
        HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect('https://{}/authorize?'.format(AUTH0_TENANT_DOMAIN)
                                + 'response_type=code&'
                                + 'client_id={}&'.format(AUTH0_CLIENT_ID)
                                + 'redirect_uri={}&'.format(AUTH0_REDIRECT_URI)
                                + 'scope=openid%20profile&'
                                + 'connection=github')

def signout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def complete_auth0(request):
    if 'code' not in request.GET:
        raise Http404()
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'code': request.GET['code'],
        'redirect_uri': AUTH0_REDIRECT_URI,
    }
    res = requests.post('https://{}/oauth/token'.format(AUTH0_TENANT_DOMAIN),
                        headers=headers,
                        data=json.dumps(payload))
    if not res.ok:
        raise Http404()
    id_token = res.json()['id_token']
    header = json.loads(base64.urlsafe_b64decode(id_token.split('.')[0]))

    res = requests.get('https://{}/.well-known/jwks.json'.format(AUTH0_TENANT_DOMAIN))
    if not res.ok:
        raise Http404()
    jwks = res.json()
    match = None
    for ii, key in enumerate(jwks['keys']):
        if key['kid'] == header['kid']:
            match = ii
            break
    if match is None:
        raise Http404()

    x5c = base64.urlsafe_b64decode(jwks['keys'][match]['x5c'][0])
    cert = load_der_x509_certificate(x5c, default_backend())
    kpem = cert.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    try:
        payload = jwt.decode(id_token,
                             key=kpem,
                             audience=AUTH0_CLIENT_ID,
                             issuer='https://{}/'.format(AUTH0_TENANT_DOMAIN))
    except:
        raise Http404()

    user = authenticate(request, remote_user=payload['sub'])
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('submit'))
    else:
        raise Http404()
