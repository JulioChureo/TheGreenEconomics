from django.urls import path

from the_green_economics.apps.dashboards.views import dashboard_home_view
from the_green_economics.apps.dashboards.views.articles_views import (
    dashboard_article_create_view,
)
from the_green_economics.apps.dashboards.views.articles_views import (
    dashboard_article_detail_view,
)
from the_green_economics.apps.dashboards.views.articles_views import (
    dashboard_article_list_view,
)
from the_green_economics.apps.dashboards.views.articles_views import (
    dashboard_article_update_view,
)
from the_green_economics.apps.dashboards.views.audits_views import audit_detail_view
from the_green_economics.apps.dashboards.views.audits_views import audit_list_view
from the_green_economics.apps.dashboards.views.news_views import (
    dashboard_news_create_view,
)
from the_green_economics.apps.dashboards.views.news_views import (
    dashboard_news_detail_view,
)
from the_green_economics.apps.dashboards.views.news_views import (
    dashboard_news_list_view,
)
from the_green_economics.apps.dashboards.views.news_views import (
    dashboard_news_update_view,
)

app_name = "dashboards"
urlpatterns = [
    path("", dashboard_home_view, name="home"),
    path("articles/", dashboard_article_list_view, name="article-list"),
    path(
        "articles/detail/<slug:slug>/",
        dashboard_article_detail_view,
        name="article-detail",
    ),
    path("articles/create/", dashboard_article_create_view, name="article-create"),
    path(
        "articles/update/<slug:slug>/",
        dashboard_article_update_view,
        name="article-update",
    ),
    path("news/", dashboard_news_list_view, name="news-list"),
    path("news/detail/<slug:slug>/", dashboard_news_detail_view, name="news-detail"),
    path("news/create/", dashboard_news_create_view, name="news-create"),
    path("news/update/<slug:slug>/", dashboard_news_update_view, name="news-update"),
    path("audits/", audit_list_view, name="audit-list"),
    path("audits/detail/<int:pk>/", audit_detail_view, name="audit-detail"),
]
