import json


class TokenMiddlewareFix(object):
    """
    Source: https://stackoverflow.com/a/46975998/5638941
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            body = json.loads(request.body)
            token = body.get("originalDetectIntentRequest", None)
            token = token.get("payload", None)
            token = token.get("user", None)
            token = token.get("accessToken", None)
            if token is not None:
                request.META["HTTP_AUTHORIZATION"] = "Bearer {}".format(token)
        except (ValueError, AttributeError):
            pass
        return self.get_response(request)
