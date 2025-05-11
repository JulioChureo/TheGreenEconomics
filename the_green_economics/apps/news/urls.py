from django.urls import path

from the_green_economics.apps.news.views import NewsDetailView
from the_green_economics.apps.news.views import NewsListView

app_name = "news"
urlpatterns = [
    path("", NewsListView.as_view(), name="list"),
    path("<slug:slug>/", NewsDetailView.as_view(), name="detail"),
]
