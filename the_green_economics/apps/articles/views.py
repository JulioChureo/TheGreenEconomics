from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import Article
from .forms import ArticleForm
from .forms import ArticleTagForm
from .forms import DeleteArticleForm
from .forms import DeleteArticleTagForm
from .models import ArticleTag


# Vistas para Artículos Científicos
class ArticleListView(ListView):
    model = Article
    template_name = "articles/articles_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return Article.objects.all().order_by("-publication_date")
        return Article.objects.filter().order_by(
            "-publication_date",
        )


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/articles_detail.html"
    context_object_name = "article"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Article.objects.all()
        return Article.objects.filter()


class ArticleCreateView( CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/articles_create.html"
    success_url = reverse_lazy("articles:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/articles_form.html"
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy("articles:detail", kwargs={"slug": self.object.slug})


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    form_class = DeleteArticleForm
    template_name = "articles/articles_confirm_delete.html"
    success_url = reverse_lazy("articles:list")
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.request.user.is_staff


# Vistas para Etiquetas
class TagListView(ListView):
    model = ArticleTag
    template_name = "articles/tag_list.html"
    context_object_name = "tags"
    paginate_by = 20


class TagCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ArticleTag
    form_class = ArticleTagForm
    template_name = "articles/tag_form.html"
    success_url = reverse_lazy("tag_list")

    def test_func(self):
        return self.request.user.is_staff


class TagUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ArticleTag
    form_class = ArticleTagForm
    template_name = "articles/tag_form.html"
    success_url = reverse_lazy("tag_list")
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.request.user.is_staff


class TagDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ArticleTag
    form_class = DeleteArticleTagForm
    template_name = "articles/tag_confirm_delete.html"
    success_url = reverse_lazy("tag_list")
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_articles"] = self.object.articles.count()
        return context

    class ArticleAuditView(LoginRequiredMixin, UserPassesTestMixin, ListView):
        model = Article
        template_name = "auditPage.html"
        context_object_name = "articles"
        queryset = Article.objects.all().order_by("-created_at")
        paginate_by = 20

        def get_queryset(self):
            if self.request.user.is_staff:
                return Article.objects.all().order_by("-publication_date")
            return Article.objects.filter(status=Article.Status.PUBLISHED).order_by("-publication_date")

