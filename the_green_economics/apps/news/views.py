from django.views.generic import DetailView
from django.views.generic import ListView

from the_green_economics.apps.news.models import News

NEWS_QUERYSET = News.objects.filter(
    status=News.Status.PUBLISHED,
).order_by("-publication_date")


class NewsListView(ListView):
    model = News
    template_name = "news/news_list.html"
    context_object_name = "news"
    paginate_by = 10
    queryset = NEWS_QUERYSET


news_list_view = NewsListView.as_view()


class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_retrieve.html"
    context_object_name = "news"
    slug_url_kwarg = "slug"
    queryset = NEWS_QUERYSET


news_detail_view = NewsDetailView.as_view()
