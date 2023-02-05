from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    # ex: api/users/login/
    path("login/", views.Login.as_view(), name="login"),
    # ex: api/users/register/
    path("register/", views.Register.as_view(), name="register"),
    # ex: api/users/loginotp/
    path("loginotp/", views.LoginOTP.as_view(), name="login_otp"),
    # ex: api/users/isunique/
    path("isunique/", views.CheckUnique.as_view(), name="check_unique"),
    # ex: api/users/changepassword/
    path("changepassword/", views.ChangePassword.as_view(), name="change_password"),
    # ex: api/users/updateprofile/
    path("updateprofile/", views.UpdateProfileView.as_view(), name="update_profile"),
    # ex: api/users/userprofile/
    path("userprofile/", views.UserProfileView.as_view(), name="user_profile"),
]
