import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str
from django.utils.translation import gettext as _
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.settings import api_settings
from six import text_type

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class JSONWebTokenAuthenticationQS(BaseAuthentication):
    """
    Token based authentication using the JSON Web Token standard.

    This is a custom JWT Authentication class.  The traditional one
    can only authenticate from Header with a specific key only.

    This model will first look into HEADER and if the key is not found
    there, it looks for key in the body.
    Key is also changeable and can be set in Django settings as
    JWT_AUTH_KEY with default value of Authorization.

    """

    key = getattr(settings, "JWT_AUTH_KEY", "Authorization")
    header_key = "HTTP_" + key.upper()
    prefix = api_settings.JWT_AUTH_HEADER_PREFIX
    cookie = api_settings.JWT_AUTH_COOKIE

    def get_authorization(self, request):
        """
        This function extracts the authorization JWT string. It first
        looks for specified key in header and then looks
        for the same in body part.

        Parameters
        ----------
        request: HttpRequest
            This is the raw request that user has sent.

        Returns
        -------
        auth: str
            Return request's 'JWT_AUTH_KEY:' content from body or
            Header, as a bytestring.

            Hide some test client ickyness where the header can be unicode.
        """

        auth = request.META.get(self.header_key, b"")

        if isinstance(auth, text_type):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def get_jwt_value(self, request):
        """
        This function has been overloaded and it returns the proper JWT
        auth string.
        Parameters
        ----------
        request: HttpRequest
            This is the request that is received by DJango in the view.
        Returns
        -------
        str
            This returns the extracted JWT auth token string.

        """

        auth = self.get_authorization(request).split()
        auth_header_prefix = self.prefix.lower() or ""

        if not auth:
            return request.COOKIES.get(self.cookie) if self.cookie else None
        if auth_header_prefix is None or len(auth_header_prefix) < 1:
            auth.append("")
            auth.reverse()

        if smart_str(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _("Invalid Authorization header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)

        elif len(auth) > 2:
            msg = _(
                "Invalid Authorization header. Credentials string "
                "should not contain spaces."
            )
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _("Signature has expired.")
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _("Error decoding signature.")
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return (user, jwt_value)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _("Invalid payload.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _("Invalid signature.")
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _("User account is disabled.")
            raise exceptions.AuthenticationFailed(msg)

        return user
