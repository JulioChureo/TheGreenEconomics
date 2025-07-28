from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from the_green_economics.apps.articles.models import Article
from the_green_economics.apps.utils.models import PublicationStatus

HOME_QUERYSET = (
    Article.objects.filter(status=PublicationStatus.PUBLISHED)
    .order_by("-created_at")[:15]
    .values("id", "title", "slug", "publication_date", "summary")
)


class HomeView(TemplateView):
    """Home view. extract the last 5 articles and news from the database"""

    template_name = "pages/home.html"

    def get_queryset(self):
        queryset = cache.get_or_set(
            "articles:home_articles",
            HOME_QUERYSET,
            timeout=60 * 15,
        )

        if queryset is None:
            queryset = HOME_QUERYSET
            cache.set("articles:home_articles", queryset, timeout=60 * 15)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = list(self.get_queryset())
        return context


home_view = HomeView.as_view()


"""@method_decorator(
    cache_page(timeout=60, key_prefix="about-view-"),
    name="dispatch",
)"""


class AboutView(TemplateView):
    """About view"""

    template_name = "pages/about.html"


about_view = AboutView.as_view()


"""@method_decorator(
    cache_page(timeout=60, key_prefix="book-view-"),
    name="dispatch",
)"""


class BookView(TemplateView):
    """Book view"""

    template_name = "pages/book.html"


book_view = BookView.as_view()
