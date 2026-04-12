from django.urls import path

from .views import about_view
from .views import book_view
from .views import home_view
from .views import desc_view

app_name = "home"

urlpatterns = [
    path("", view=home_view, name="home"),
    path("about/", view=about_view, name="about"),
    path("book/", view=book_view, name="book"),
    path("description/", view=desc_view, name="OJS"),
]
