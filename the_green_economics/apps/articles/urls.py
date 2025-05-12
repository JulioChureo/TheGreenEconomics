from django.urls import path

from the_green_economics.apps.articles.views import article_detail_view
from the_green_economics.apps.articles.views import article_list_view

app_name = "articles"
urlpatterns = [
    path("", article_list_view, name="list"),
    path("<slug:slug>/", article_detail_view, name="detail"),
]
