from django.urls import path

from full_backup_web_app.views import auth_login, home, signup, auth_logout, source_dir_func, dest_dir_func, start_backup

urlpatterns = [
    path("", auth_login, name="login"),
    path("signup/", signup, name="signup"),
    path("home/", home, name="home"),
    path("home/source/", source_dir_func, name="source"),
    path("home/destination/", dest_dir_func, name="destination"),
    path("home/start_backup", start_backup, name="start_backup"),
    path("logout/", auth_logout, name="logout"),
]
