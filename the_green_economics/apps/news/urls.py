from django.urls import path

from .views import NewsCreateView
from .views import NewsDeleteView
from .views import NewsDetailView
from .views import NewsListView
from .views import NewsTagCreateView
from .views import NewsTagDeleteView
from .views import NewsTagListView
from .views import NewsTagUpdateView
from .views import NewsUpdateView

app_name = "news"
urlpatterns = [
    path("", NewsListView.as_view(), name="list"),
    path("<slug:slug>/", NewsDetailView.as_view(), name="detail"),
    path("create/", NewsCreateView.as_view(), name="create"),
    path("update/<slug:slug>/", NewsUpdateView.as_view(), name="update"),
    path("delete/<slug:slug>/", NewsDeleteView.as_view(), name="delete"),
    path("tags/", NewsTagListView.as_view(), name="tag-list"),
    path("tags/create/", NewsTagCreateView.as_view(), name="tag-create"),
    path("tags/update/<slug:slug>/", NewsTagUpdateView.as_view(), name="tag-update"),
    path("tags/delete/<slug:slug>/", NewsTagDeleteView.as_view(), name="tag-delete"),
]
