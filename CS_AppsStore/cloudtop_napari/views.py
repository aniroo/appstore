from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from time import sleep

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from cloudtop_napari import deployment


# Create your views here.
@login_required
def login_start(request):
    # view function when the start action is triggered from CommonsShare Apps Store from
    # which the user has already logged in to CommonsShare Apps Store directly
    redirect_url = deploy(request)
    messages.success(request, 'Launching CloudTop/Napari')
    return HttpResponseRedirect(redirect_url)


@login_required
def deploy(request):
    print("deploying napari...")

    print(f"USERNAME: {request.user.username}")
    request.META['REMOTE_USER'] = request.user.username
    print(f"REQUEST META: {request.META}")
    request.session['REMOTE_USER'] = request.user.username

    try:
        redirect_url = deployment.deploy(request)
    except Exception as ex:
        print(ex, "extend")
        return JsonResponse(data={'invalid ip_address or port from napari deployment ': ex},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

    sleep(20)
    return redirect_url
