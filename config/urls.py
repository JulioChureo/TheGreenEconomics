from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views import defaults as default_views

urlpatterns = [
    # --- Django JET URLS ---
    path("jet/", include("jet.urls", "jet")),  # Django JET URLS
    path(
        "jet/dashboard/",
        include("jet.dashboard.urls", "jet-dashboard"),
    ),  # Django JET dashboard URLS
    # --- Django Admin, use {% url 'admin:index' %} ---
    path(settings.ADMIN_URL, admin.site.urls),
    # --- app URLS ---
    path("", include("the_green_economics.apps.pages.urls", namespace="pages")),
    path("users/", include("the_green_economics.apps.users.urls", namespace="users")),
    path(
        "articles/",
        include("the_green_economics.apps.articles.urls", namespace="articles"),
    ),
    path("news/", include("the_green_economics.apps.news.urls", namespace="news")),
    path("", include("the_green_economics.apps.contacts.urls", namespace="contacts")),
    path(
        "dashboards/",
        include("the_green_economics.apps.dashboards.urls", namespace="dashboards"),
    ),
    path("i18n/", include("django.conf.urls.i18n")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
            *urlpatterns,
        ]
