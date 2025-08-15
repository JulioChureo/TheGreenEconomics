from django.core.cache import cache
from django.views.generic import TemplateView

from the_green_economics.apps.articles.querysets import HOME_QUERYSET


class HomeView(TemplateView):
    """Home view. extract the last 5 articles and news from the database"""

    template_name = "pages/home.html"

    def get_queryset(self):
        """queryset = cache.get_or_set(
            "articles:home_articles",
            HOME_QUERYSET,
            timeout=60 * 15,
        )

        if queryset is None:
            queryset = HOME_QUERYSET
            cache.set("articles:home_articles", queryset, timeout=60 * 15)"""
        return HOME_QUERYSET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = tuple(self.get_queryset())
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
