from django.urls import path

from .views import ArticleCreateView
from .views import ArticleDeleteView
from .views import ArticleDetailView
from .views import ArticleListView
from .views import ArticleUpdateView
from .views import TagCreateView
from .views import TagDeleteView
from .views import TagListView
from .views import TagUpdateView

app_name = "articles"
urlpatterns = [
    path("", ArticleListView.as_view(), name="list"),
    path("detail/<slug:slug>/", ArticleDetailView.as_view(), name="detail"),
    path("create/", ArticleCreateView.as_view(), name="create"),
    path("update/<slug:slug>/", ArticleUpdateView.as_view(), name="update"),
    path("delete/<slug:slug>/", ArticleDeleteView.as_view(), name="delete"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/create/", TagCreateView.as_view(), name="tag-create"),
    path("tags/update/<slug:slug>/", TagUpdateView.as_view(), name="tag-update"),
    path("tags/delete/<slug:slug>/", TagDeleteView.as_view(), name="tag-delete"),
]
