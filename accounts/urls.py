from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "accounts"

urlpatterns = [
    path("welcome/", views.welcome_view, name="welcome"),
    path("login/", views.email_login_view, name="email_login"),
    path("verify/", views.verify_code_view, name="verify_code"),
    path("signup/", views.signup_view, name="signup"),

    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit_view, name="profile_edit"),

    path("logout/", LogoutView.as_view(next_page="accounts:email_login"), name="logout"),
]
