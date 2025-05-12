from django.urls import path

from the_green_economics.apps.users.views import user_log_out_view
from the_green_economics.apps.users.views import user_login_view

app_name = "users"
urlpatterns = [
    path("login/", view=user_login_view, name="login"),
    path("logout/", view=user_log_out_view, name="logout"),
]
