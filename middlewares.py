#-*- coding: utf-8 -*-


class TwitterAPIMiddleware(object):

    def process_request(self, request):
        assert hasattr(request, 'session')
        request.__class__.twitter_api = TwitterAPIHandler()
        return None


class TwitterAPIHandler(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_twitter_api'):
            from . import get_api
            request._cached_twitter_api = get_api(request)

        return request._cached_twitter_api
