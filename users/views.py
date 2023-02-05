import logging

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from drfaddons.utils import validate_email, JsonResponse
from drfaddons.views import ValidateAndPerformView
from redis.client import Redis
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.mixins import status
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from core.utils import get_redis_conn
from users.constants import OTPValidationType
from users.serializers import (
    ForgotPasswordSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
    OTPVerify,
    CheckUniqueSerializer,
    UpdateProfileSerializer,
)
from users.tasks import send_welcome_email_async
from users.utils import login_user, check_unique, generate_otp, send_otp, validate_otp

logger = logging.getLogger(__name__)

User = get_user_model()


class Register(ValidateAndPerformView):
    """
    This Registers a new User to the system.
    """

    serializer_class = UserRegisterSerializer

    def validated(self, serialized_data, *args, **kwargs):
        redis: Redis = get_redis_conn()
        email = serialized_data.initial_data["email"]
        mobile = serialized_data.initial_data["mobile"]
        lock_str = f"register_lock:{email}:{mobile}"
        with redis.lock(lock_str, timeout=5, blocking_timeout=0):
            user = User.objects.create_user(
                username=serialized_data.initial_data["username"],
                email=email,
                name=serialized_data.initial_data["name"],
                password=serialized_data.initial_data["password"],
                mobile=mobile,
                is_active=True,
            )

        data = {
            "name": user.get_full_name(),
            "username": user.get_username(),
            "id": user.id,
            "email": user.email,
            "mobile": user.mobile,
        }
        status_code = status.HTTP_201_CREATED
        send_welcome_email_async(user.email)

        return data, status_code


class Login(ValidateAndPerformView):
    """
    This is used to Login into system. The data required are 'username' and 'password'.
    In 'username' user can provide either username or mobile or email address.
    """

    serializer_class = JSONWebTokenSerializer

    @csrf_exempt
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return JsonResponse(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        user = serializer.validated_data["user"]
        data, status_code = login_user(user, request)
        return JsonResponse(data, status=status_code)


class CheckUnique(ValidateAndPerformView):
    """
    This view checks if the given property -> value pair is unique (or doesn't exists yet)
    'prop': A property to check for uniqueness (username/email/mobile)
    'value': Value against property which is to be checked for.
    """

    serializer_class = CheckUniqueSerializer

    def validated(self, serialized_data, *args, **kwargs):
        return (
            {
                "unique": check_unique(
                    serialized_data.initial_data["prop"],
                    serialized_data.initial_data["value"],
                )
            },
            status.HTTP_200_OK,
        )


class LoginOTP(ValidateAndPerformView):
    serializer_class = OTPVerify

    def validated(self, serialized_data, *args, **kwargs):
        otp = serialized_data.data["otp"]
        value = serialized_data.data["value"]

        user = User.objects.filter(Q(mobile=value) | Q(email=value)).first()
        if not user:
            data = {
                "success": False,
                "message": "No user exists with provided details!",
            }
            status_code = status.HTTP_404_NOT_FOUND
            return data, status_code

        if otp is None:
            prop = OTPValidationType.EMAIL if validate_email(value) else OTPValidationType.MOBILE
            otp_obj = generate_otp(prop, value)
            data = send_otp(prop, value, otp_obj, user.email)
            status_code = status.HTTP_201_CREATED if data["success"] else status.HTTP_400_BAD_REQUEST

            return data, status_code

        data, status_code = validate_otp(value, int(otp))
        if status_code == status.HTTP_202_ACCEPTED:
            data, status_code = login_user(user, self.request)

        return data, status_code


class ChangePassword(UpdateAPIView):
    """
    This view will let the user change the password.
    """

    queryset = User.objects.all()
    serializer_class = ForgotPasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return JsonResponse({"success": True}, status=status.HTTP_202_ACCEPTED)


class UpdateProfileView(UpdateAPIView):
    """
    This view is to update a user profile.
    """

    queryset = User.objects.all()
    serializer_class = UpdateProfileSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.perform_update(serializer)
            request.user.save()
            return JsonResponse(serializer.validated_data, status=status.HTTP_202_ACCEPTED)
        except IntegrityError as e:
            raise ValidationError("Given mobile number or email is already registered.") from e


class UserProfileView(ListAPIView):
    """
    This view will list the user details based on the access token
    get: Lists the single user instance
    """

    pagination_class = None
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.pk)
