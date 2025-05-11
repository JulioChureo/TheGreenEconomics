from django.views.generic import DetailView
from django.views.generic import ListView

from the_green_economics.apps.news.models import News


class NewsListView(ListView):
    model = News
    template_name = "news/news_list.html"
    context_object_name = "news"
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = News.objects.all().order_by("-publication_date")
        else:
            queryset = News.objects.filter(status=News.Status.PUBLISHED).order_by(
                "-publication_date",
            )
        return queryset


news_list_view = NewsListView.as_view()


class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_retrieve.html"
    context_object_name = "news"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        if self.request.user.is_staff:
            return News.objects.all()
        return News.objects.filter(status=News.Status.PUBLISHED)


news_detail_view = NewsDetailView.as_view()
