from django.urls import path

from .views import HomeView, PublicaConNosotrosView

app_name = "home"

urlpatterns = [
    path("", view=HomeView.as_view(), name="home"),
    path("publish/", view=PublicaConNosotrosView.as_view(), name="publish"),  
]
