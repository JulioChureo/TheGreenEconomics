import django_filters
from django.utils.translation import gettext_lazy as _

from the_green_economics.apps.articles.models import Article
from the_green_economics.apps.articles.models import ArticleTag


class ArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label=_("article:filter_title_label"),
        help_text=_("article:filter_title_help_text"),
        field_name="title",
        lookup_expr="icontains",
    )

    class Meta:
        model = Article
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["title"].field.widget.attrs["placeholder"] = kwargs.get(
            "title_placeholder",
            "Buscar por título",
        )
        self.filters["title"].field.widget.attrs["class"] = "w-full"


class ArticleTagFilter(django_filters.FilterSet):
    class Meta:
        model = ArticleTag
        fields = ["tag", "slug"]
        labels = {
            "tag": _("article_tag:filter_name_label"),
            "slug": _("article_tag:filter_slug_label"),
        }
        help_texts = {
            "tag": _("article_tag:filter_name_help_text"),
            "slug": _("article_tag:filter_slug_help_text"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["tag"].field.widget.attrs["class"] = "w-full"
        self.filters["slug"].field.widget.attrs["class"] = "w-full"
        self.filters["tag"].field.widget.attrs["placeholder"] = "Nombre de la etiqueta"
        self.filters["slug"].field.widget.attrs["placeholder"] = "Slug de la etiqueta"
        self.filters["tag"].field.widget.attrs["autocomplete"] = "off"
