from django.urls import path

from .views import ContactView
from .views import HomeView

app_name = "home"

urlpatterns = [
    path("", view=HomeView.as_view(), name="home"),
    path("publish/", view=ContactView.as_view(), name="publish"),
]
