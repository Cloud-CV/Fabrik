# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.contrib.auth.models import User


def check_login(request):
    try:
        if request.GET.get('isOAuth') == 'false':
            username = request.GET['username']
            password = request.GET['password']
            user = User.objects.get(username=username)
            user_id = user.id

            if not user.check_password(password):
                return JsonResponse({
                    'result': False,
                    'error': 'Please enter valid credentials'
                })

            is_authenticated = user.is_authenticated()
            if (is_authenticated):
                username = user.username

            return JsonResponse({
                'result': is_authenticated,
                'user_id': user_id,
                'username': username,
            })
        else:
            user = User.objects.get(username=request.user.username)
            user_id = user.id
            username = 'Anonymous'

            is_authenticated = user.is_authenticated()
            if (is_authenticated):
                username = user.username

            return JsonResponse({
                'result': is_authenticated,
                'user_id': user_id,
                'username': username
            })
    except Exception as e:
        return JsonResponse({
            'result': False,
            'error': str(e)
        })
