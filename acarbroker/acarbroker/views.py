"""

SCL <scott@rerobots.net>
2018
"""
from __future__ import absolute_import

import base64
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import views
from . import tasks
from .models import SimJob


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'acarbroker/signin.html')
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
    context['jobs'] = []
    try:
        for job in SimJob.objects.iterator():
            context['jobs'].append({
                'starttime': job.starttime,
                'result': job.result,
                'done': job.done,
            })
    except:
        pass
    return render(request, 'acarbroker/index.html', context)


def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if 'username' in request.POST and 'password' in request.POST:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'acarbroker/signin.html')
