from django.core.cache import cache
from django.views.generic import TemplateView

from the_green_economics.apps.articles.models import Article

HOME_QUERYSET = (
    Article.objects.all()
    .order_by("-created_at")[:15]
    .values("id", "title", "slug", "publication_date", "summary")
)


class HomeView(TemplateView):
    """Home view. extract the last 5 articles and news from the database"""

    template_name = "pages/home.html"

    def get_queryset(self):
        queryset = cache.get_or_set(
            "home-articles",
            HOME_QUERYSET,
            timeout=60 * 15,
        )

        if queryset is None:
            queryset = HOME_QUERYSET
            cache.set("home-articles", queryset, timeout=60 * 15)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = list(self.get_queryset())
        return context


home_view = HomeView.as_view()


class AboutView(TemplateView):
    """About view"""

    template_name = "pages/about.html"


about_view = AboutView.as_view()


class BookView(TemplateView):
    """Book view"""

    template_name = "pages/book.html"


book_view = BookView.as_view()
