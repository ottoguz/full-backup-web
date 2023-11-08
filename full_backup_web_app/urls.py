from django.urls import path

from full_backup_web_app.views import auth_login, home

urlpatterns = [
    path("", auth_login, name="login"),
    path("home/", home, name="home")
]
