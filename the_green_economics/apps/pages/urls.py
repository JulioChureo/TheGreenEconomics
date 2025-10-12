from django.urls import path

from .views import about_view
from .views import book_read_view
from .views import book_view
from .views import home_view

app_name = "home"

urlpatterns = [
    path("", view=home_view, name="home"),
    path("about/", view=about_view, name="about"),
    path("book/", view=book_view, name="book"),
    path("read/", view=book_read_view, name="book_read"),
]
