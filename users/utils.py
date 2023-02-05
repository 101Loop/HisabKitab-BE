import datetime
import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from drfaddons.utils import get_client_ip, send_message
from rest_framework import status
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler

from users.models import AuthTransaction, OTPValidation

User = get_user_model()


def random_number_token(length=6):
    """
    Returns a string of random digits encoded as string.
    :param int length: The number of digits to return.
    :returns: A string of decimal digits.
    :rtype: str

    # Copied from https://github.com/django-otp/django-otp/blob/master/src/django_otp/util.py
    """
    rand = random.SystemRandom()
    return "".join(rand.choices(string.digits, k=length))


def check_unique(prop, value):
    """
    This function checks if the value provided is present in Database or can be created in DBMS as unique data.
    Parameters
    ----------
    prop: str
        The model property to check for. Can be::
            email
            mobile
            username
    value: str
        The value of the property specified

    Returns
    -------
    bool
        True if the data sent doesn't exist, False otherwise.
    Examples
    --------
    To check if test@testing.com email address is already present in Database
    >>> print(check_unique('email', 'test@testing.com'))
    True
    """
    user = User.objects.extra(where=[f"{prop} = '{value}'"])
    return user.count() == 0


def generate_otp(prop, value) -> OTPValidation:
    """
    This function generates an OTP and saves it into Model. It also sets various counters, such as send_counter,
    is_validated, validate_attempt.
    Parameters
    ----------
    prop: str
        This specifies the type for which OTP is being created. Can be::
            email
            mobile
    value: str
        This specifies the value for which OTP is being created.

    Returns
    -------
    otp_object: OTPValidation
        This is the instance of OTP that is created.
    Examples
    --------
    To create an OTP for an Email test@testing.com
    >>> print(generate_otp('email', 'test@testing.com'))
    OTPValidation object

    >>> print(generate_otp('email', 'test@testing.com').otp)
    5039164
    """
    # Get or Create new instance of Model with value of provided value and set proper counter.
    otp_object, created = OTPValidation.objects.get_or_create(destination=value)
    if not created and otp_object.reactive_at > datetime.datetime.now():
        return otp_object

    # Create a random number
    random_number = get_random_string(
        length=7, allowed_chars=settings.ALLOWED_OTP_CHARACTERS
    )
    # Checks if random number is unique among non-validated OTPs and creates new until it is unique.
    while (
        OTPValidation.objects.filter(otp__exact=random_number)
        .filter(is_validated=False)
        .exists()
    ):
        # using a different random number generator here because it's quite difficult to write
        # tests for this otherwise because it'll keep generating the same number over and over
        random_number = random_number_token(length=7)

    otp_object.otp = random_number
    otp_object.type = prop
    # Set is_validated to False
    otp_object.is_validated = False
    # Set attempt counter to 3, user has to enter correct OTP in 3 chances.
    otp_object.validate_attempt = 3
    otp_object.reactive_at = datetime.datetime.now() - datetime.timedelta(minutes=1)
    otp_object.save()
    return otp_object


def validate_otp(value, otp):
    """
    This function is used to validate the OTP for a particular value.
    It also reduces the attempt count by 1 and resets OTP.
    Parameters
    ----------
    value: str
        This is the unique entry for which OTP has to be validated.
    otp: int
        This is the OTP that will be validated against one in Database.

    Returns
    -------
    tuple
        Returns a tuple containing::
                data: dict
                    This is a dictionary containing::
                        'success': bool
                            This will be True if OTP is validated, else False
                        'OTP': str
                            This will contain a proper message about the OTP Validation
                status: int
                    This will be a HTTP Status Code with resepect to the type of success or error occurred.
    Examples
    --------
    To validate an OTP against test@testing.com with wrong OTP
    >>> print(validate_otp('test@testing.com', 6518631))
    ({'OTP': 'OTP Validation failed! 2 attempts left!', 'success': False}, 401)

    To validate an OTP against random@email.com with value that doesn't exist
    >>>print(validate_otp('random@email.com', 6518631))
    ({'OTP': 'Provided value to verify not found!', 'success': False}, 404)

    To validate a correct OTP with value test@testing.com
    >>>print(validate_otp('test@testing.com', 5039164))
    ({'OTP': 'OTP Validated successfully!', 'success': True}, 202)

    To validate incorrect OTP more than 3 times or re-validate already validated value with incorrect OTP
    >>>print(validate_otp('test@testing.com', 6518631))
    ({'OTP': 'Attempt exceeded! OTP has been reset!', 'success': False}, 401)
    """
    # Initialize data dictionary that will be returned
    data = {"success": False}
    try:
        # Try to get OTP Object from Model and initialize data dictionary
        otp_object = OTPValidation.objects.get(destination=value)
        # Decrement validate_attempt
        otp_object.validate_attempt -= 1
        if str(otp_object.otp) == str(otp):
            otp_object.is_validated = True
            otp_object.save()
            data["OTP"] = "OTP Validated successfully!"
            data["success"] = True
            status_code = status.HTTP_202_ACCEPTED
        elif otp_object.validate_attempt <= 0:
            generate_otp(otp_object.type, value)
            status_code = status.HTTP_401_UNAUTHORIZED
            data["OTP"] = "Attempt exceeded! OTP has been reset!"
        else:
            otp_object.save()
            data[
                "OTP"
            ] = f"OTP Validation failed! {otp_object.validate_attempt} attempts left!"
            status_code = status.HTTP_401_UNAUTHORIZED
    except OTPValidation.DoesNotExist:
        # If OTP object doesn't exist set proper message and status_code
        data["OTP"] = f"Provided {value=} to verify not found!"
        status_code = status.HTTP_404_NOT_FOUND

    return data, status_code


def send_otp(prop: str, value: str, otpobj: OTPValidation, recip: str) -> dict:
    """
    This function sends OTP to specified value.
    Parameters
    ----------
    prop: str
        This is the type of value. It can be "email" or "mobile"
    value: str
        This is the value at which and for which OTP is to be sent.
    otpobj: OTPValidation
        This is the OTP or One Time Passcode that is to be sent to user.
    recip: str
        This is the recipient to whom EMail is being sent. This will be deprecated once SMS feature is brought in.

    Returns
    -------

    """
    otp = otpobj.otp

    rdata = {"success": False, "message": None}

    if otpobj.reactive_at > datetime.datetime.now():
        rdata[
            "message"
        ] = f"OTP sending not allowed until: {otpobj.reactive_at.strftime('%d-%h-%Y %H:%M:%S')}"
        return rdata

    message = (
        f"OTP for verifying {prop}: {value} is {otp}. Don't share this with anyone!"
    )

    subject = "OTP for Verification"
    rdata = send_message(
        message=message, subject=subject, recip_email=[recip], recip=[recip]
    )

    if rdata["success"]:
        otpobj.reactive_at = datetime.datetime.now() + datetime.timedelta(minutes=3)
        otpobj.save()

    return rdata


def login_user(user: User, request) -> (dict, int):
    token = jwt_encode_handler(jwt_payload_handler(user))
    user.last_login = datetime.datetime.now()
    user.save()
    AuthTransaction(
        user=user,
        ip_address=get_client_ip(request),
        token=token,
        session=user.get_session_auth_hash(),
    ).save()

    data = {"session": user.get_session_auth_hash(), "token": token}
    status_code = status.HTTP_200_OK
    return data, status_code


def check_validation(value: str) -> bool:
    """
    This functions check if given value is already validated via OTP or not.
    Bypassed for FlexyManagers
    Parameters
    ----------
    value: str
        This is the value for which OTP validation is to be checked.

    Returns
    -------
    bool
        True if value is validated, False otherwise.
    Examples
    --------
    To check if 'test@testing.com' has been validated!
    >>> print(check_validation('test@testing.com'))
    True

    """
    try:
        return OTPValidation.objects.values_list("is_validated", flat=True).get(
            destination=value
        )
    except OTPValidation.DoesNotExist:
        return False
