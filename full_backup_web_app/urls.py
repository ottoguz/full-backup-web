from django.urls import path

from full_backup_web_app.views import auth_login, home, signup, auth_logout

urlpatterns = [
    path("", auth_login, name="login"),
    path("signup/", signup, name="signup"),
    path("home/", home, name="home"),
    path("logout/", auth_logout, name="logout"),
]
