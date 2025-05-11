from django.urls import path

from the_green_economics.apps.articles.views import ArticleDetailView
from the_green_economics.apps.articles.views import ArticleListView

app_name = "articles"
urlpatterns = [
    path("", ArticleListView.as_view(), name="list"),
    path("<slug:slug>/", ArticleDetailView.as_view(), name="detail"),
]
