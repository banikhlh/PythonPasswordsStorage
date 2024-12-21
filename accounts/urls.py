from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("verify_email/", views.verify_email, name="verify_email"),
    path("reverify_email/", views.reverify_email, name="resend_verification_email"),
    path("recovery_signin/", views.recovery_signin, name="recovery_signin"),
    path("recovery_phrase/", views.phrase, name="recovery_phrase"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
