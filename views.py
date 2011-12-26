#-*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
import tweepy

from . import get_oauth_handler, get_api_handler, twitter_login
from . import models


def login(request):
    oauth = get_oauth_handler()
    authorization_url = oauth.get_authorization_url()
    models.RequestToken.objects.create(
        key=oauth.request_token.key,
        secret=oauth.request_token.secret)

    return HttpResponseRedirect(authorization_url)


def authorization(request):
    oauth = get_oauth_handler()
    token_key = request.GET.get('oauth_token', '')
    verifier = request.GET.get('oauth_verifier', '')

    try:
        token = models.RequestToken.objects.get(key=token_key)
    except models.RequestToken.DoesNotExist:
        return HttpResponseRedirect('/login')
    else:
        oauth.set_request_token(token.key, token.secret)
        try:
            access_token = oauth.get_access_token(verifier)
            api = get_api_handler(access_token)
            userid = api.me().id
        except tweepy.TweepError:
            pass
        else:
            access_token, created = models.AccessToken.objects.get_or_create(
                                        userid=userid,
                                    )
            if not (access_token.key is oauth.access_token.key and\
            access_token.secret is oauth.access_token.secret):
                access_token.key = oauth.access_token.key
                access_token.secret = oauth.access_token.secret
                access_token.save()

            twitter_login(request, userid)
        finally:
            token.delete()
            return HttpResponseRedirect('/')


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/')
