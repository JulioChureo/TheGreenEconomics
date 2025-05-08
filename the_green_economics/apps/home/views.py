from django.views.generic import TemplateView

from the_green_economics.apps.articles.models import Article
from the_green_economics.apps.news.models import News


class HomeView(TemplateView):
    """Home view. extract the last 5 articles and news from the database"""

    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["articles"] = Article.objects.all().order_by("-date")[:5]
        context["news"] = News.objects.all().order_by("-created_at")[:5]
        return context
