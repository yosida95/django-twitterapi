#-*- coding: utf-8 -*-

import tweepy
from django.conf import settings
from . import models


SESSION_KEY = u'_twitter_id'


def get_oauth_handler():
    return tweepy.OAuthHandler(
               settings.TWITTER_CONSUMER_KEY,
               settings.TWITTER_CONSUMER_SECRET)


def get_api_handler(access_token=None):
    if hasattr(access_token, 'key') and hasattr(access_token, 'secret'):
        oauth = get_oauth_handler()
        print access_token.key, access_token.secret
        oauth.set_access_token(access_token.key, access_token.secret)
        return tweepy.API(auth_handler=oauth)

    else:
        return tweepy.api


def get_api(request):
    try:
        userid = request.session.get(SESSION_KEY, u'')
        access_token = models.AccessToken.objects.get(userid=userid)
    except models.AccessToken.DoesNotExist:
        api = tweepy.api
    else:
        api = get_api_handler(access_token)
    finally:
        return api


def twitter_login(request, userid):
    assert hasattr(request, 'session')
    request.session.flush()
    request.session[SESSION_KEY] = userid
