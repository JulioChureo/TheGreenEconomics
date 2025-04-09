from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import DeleteNewsForm
from .forms import DeleteNewsTagForm
from .forms import NewsForm
from .forms import NewsTagForm
from .models import News
from .models import NewsTag


class NewsListView(ListView):
    model = News
    template_name = "news/news_list.html"
    context_object_name = "news"
    paginate_by = 10

    def get_queryset(self):
        cache_key = f"news_list_{self.request.user.is_staff}"
        queryset = cache.get(cache_key)

        if not queryset:
            if self.request.user.is_staff:
                queryset = News.objects.all().order_by("-publication_date")
            else:
                queryset = News.objects.filter(status=News.Status.PUBLISHED).order_by(
                    "-publication_date",
                )

            cache.set(cache_key, queryset, 60 * 15)  # Cache por 15 minutos

        return queryset


class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_retrieve.html"
    context_object_name = "news"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        if self.request.user.is_staff:
            return News.objects.all()
        return News.objects.filter(status=News.Status.PUBLISHED)


class NewsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = "news/news_create.html"
    success_url = reverse_lazy("news_list")

    def test_func(self):
        if not self.request.user:
            return False
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete(f"news_list_{True}")  # Limpiar cache de administradores
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Crear Nueva Noticia")
        return context


class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = "news/news_update.html"
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy("news_detail", kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete_many(
            [f"news_list_{True}", f"news_list_{False}", f"news_{self.object.slug}"]
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Editar Noticia")
        return context


class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    form_class = DeleteNewsForm
    template_name = "news/news_delete.html"
    success_url = reverse_lazy("news_list")
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        cache.delete_many(
            [
                f"news_list_{True}",
                f"news_list_{False}",
                f"news_{self.get_object().slug}",
            ],
        )
        return super().delete(request, *args, **kwargs)


# Vistas para Etiquetas
class NewsTagListView(ListView):
    model = NewsTag
    template_name = "articles/NewsTag_list.html"
    context_object_name = "NewsTags"
    paginate_by = 20


class NewsTagCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = NewsTag
    form_class = NewsTagForm
    template_name = "articles/NewsTag_form.html"
    success_url = reverse_lazy("NewsTag_list")

    def test_func(self):
        return self.request.user.is_staff


class NewsTagUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NewsTag
    form_class = NewsTagForm
    template_name = "articles/NewsTag_form.html"
    success_url = reverse_lazy("NewsTag_list")
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.request.user.is_staff


class NewsTagDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = NewsTag
    form_class = DeleteNewsTagForm
    template_name = "articles/NewsTag_confirm_delete.html"
    success_url = reverse_lazy("NewsTag_list")
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_articles"] = self.object.articles.count()
        return context
